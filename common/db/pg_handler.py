from contextlib import contextmanager
import weakref

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists

from common.constants import DEFAULT_SCHEMAS_TO_LOAD
from common.common_utils.control_utils import (
    get_postgresql_server_address, get_postgresql_username_password, get_postgresql_dbname
)
from common.common_utils.pg_models import Base, tables_to_create

"""
NOTE:
1. The creation of engine object in sqlalchemy will actually create a postgresql connection. The session derived from
sqlalchemy engine object is totally different from the postgresql connection, they are irrelevant.
2. Currently the maximum postgresql connection limit is set to 100, including connections from all modules to
postgres container.

Usage:
If we want to access "pg_infra_sql_db" database in postgres using default username/password/host, then we will
1. Initiate an PgHandler instance by running: pg = PgHandler("pg_infra_sql_db")
2. Using context manager when you want to do postgres operation: with pg.get_session() as session
3. select example: from common.common_utils.pg_models import ddn_node_linkage
                   rows = session.query(ddn_node_linkage).filter(ddn_node_linkage.ddn_id == "12345").all()
                   for row in rows
                       print(row.ddn_id)
   insert example: new_ddn_node_linkage_row = ddn_node_linkage(ddn_id="123456", ddn_name="test_ddn_name",
                                                             node_id="test_node_id", node_type=3,
                                                             log_timestamp="2020-04-11 07:18:22.000000")
                   session.add(new_ddn_node_linkage_row)
   update example: (session
                    .query(ddn_node_linkage)
                    .filter(ddn_node_linkage.ddn_id == "12345")
                    .update({ddn_node_linkage.node_id:"new node id"}))
   delete example: rows = session.query(ddn_node_linkage).filter(ddn_node_linkage.ddn_id == "12345").all()
                   for row in rows:
                      session.delete(row)
   upsert example: entry = sql_column_labels(tf_loc=tf_loc, col_name=col_name, tag_type=PII_TAG,
                                          pii_field_name=pii_field_name,
                                          customized_pii_field_name=customized_pii_field_name)
                   session.merge(entry)
                   If you encounter any unexpected behaviors out of merge(), please refer to the link below for
                   potential solutions:
                   https://stackoverflow.com/questions/1849567/can-sqlalchemys-session-merge-update-its-
                   result-with-newer-data-from-the-data
Refs:
https://www.compose.com/articles/using-postgresql-through-sqlalchemy/
https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
https://docs.sqlalchemy.org/en/13/orm/session_basics.html
"""


class PgHandler:
    def __init__(self, database=None, host=None, username=None, password=None):
        # get database/host/username/password for postgres connection
        self.host = host if host else get_postgresql_server_address()
        self.database = database or get_postgresql_dbname()
        if username and password:
            self.username = username
            self.password = password
        else:
            self.username, self.password = get_postgresql_username_password()

        self.session_maker_with_expiration = None
        self.session_maker_without_expiration = None
        self.engine = None
        self._finalizer = None

        self.prepare()

    def prepare(self):
        """
        This function manually creates a postgres orm engine and then get a link to the engine.
        """
        self.engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.host}:5432/{self.database}',
                                    pool_pre_ping=True)
        # Define the finalizer to destroy the engine object explicitly, so that the actual postgresql connection will be
        # released.
        # NOTE, closing the session which is derived from engine object will not close the actual postgresql connection.
        self._finalizer = weakref.finalize(self, self.engine.dispose)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        self.session_maker_with_expiration = sessionmaker(self.engine, expire_on_commit=True)
        self.session_maker_without_expiration = sessionmaker(self.engine, expire_on_commit=False)

    def create_schemas(self, schema_list=()):
        """
        This function creates schemas in postgre sql DB. If the schema_list is not empty, then it will create the
        specified schemas one by one. If there's no input schema_list, it will create the schemas in default schema list
        :param schema_list: list of str. list of schema name
        """
        if not self.engine:
            self.prepare()
        if not schema_list:
            schema_list = DEFAULT_SCHEMAS_TO_LOAD
        for schema in schema_list:
            if not self.engine.dialect.has_schema(self.engine, schema):
                self.engine.execute(CreateSchema(schema))

    def create_tables(self):
        """
        This function creates all the tables defined in pg_models.py. And all the table classes defined in pg_models.py
        must inherit `Base` class initiated in pg_models.py.
        """
        if not self.engine:
            self.prepare()
        Base.metadata.create_all(self.engine, [tab.__table__ for tab in tables_to_create])

    @contextmanager
    def get_session(self, expire_on_commit=True):
        """
        This function returns SqlAlchemy ORM session. This session can be used directly to do operations like select,
        insert, update and delete to postgres.

        NOTE, the returned session is not thread safe. It recommends to use this session in non-concurrent fashion.
        Ref: https://docs.sqlalchemy.org/en/13/orm/session_basics.html
        And you MUST use context manager to manage it, for example:
            with get_session() as session:
                session.query(File).all()
        You CAN NOT use get_session like this way:
            session = get_session()
            session.query(File).all()
        Otherwise it will throw error.

        NOTE NOTE NOTE: The select query will not be executed unless you call '.all()' directly or read the query
        without '.all()'.
        The query will not be executed if you do:
            res = session.query(File)
        The query will be executed if you do:
            res = session.query(File).all()
        or
            res = session.query(File)
            res_list = [row.file_name for row in res] (This is the line where the query execution happens)

        :param: expire_on_commit: bool. True, you can only read the query results within the session. Query results will
                                        expire after session closes.
                                        False, you can still access the query results outside the session. Query results
                                        won't expire after session closes.
        :return: a live postgres sql session.
        """
        if not self.session_maker_with_expiration or not self.session_maker_without_expiration:
            self.prepare()
        if expire_on_commit:
            session = self.session_maker_with_expiration()
        else:
            session = self.session_maker_without_expiration()

        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_core_session(self):
        """
        This function returns SqlAlchemy core session that can accept raw query and non-orm query syntax.
        Please DO NOT use raw query at your first choice, only if you can not use orm query with `get_session`.

        Usage:
        1. use with context manager (RECOMMENDED)
        with pg.get_raw_query_session() as session:
            rows = session.execute(sqlalchemy.text("SELECT tf_loc FROM api.pii_tf \
                WHERE flat_data_type_tag->>'PII_FIELD_NAME' = 'GENDER';"))
            for row in rows:
                print(row)

        2. without context manager
        conn = pg.get_raw_query_session()
        rows = session.execute(sqlalchemy.text("SELECT tf_loc FROM api.pii_tf \
                WHERE flat_data_type_tag->>'PII_FIELD_NAME' = 'GENDER';"))
        for row in rows:
            print(row)
        rows.close()

        :return: a SqlAlchemy Connection object.
        """
        if not self.engine:
            self.prepare()
        return self.engine.connect()
