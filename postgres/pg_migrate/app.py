import time

from common.common_utils.pg_handler import PgHandler
from common.helios_uuid import get_uuid
from common.log import log, svc_logging, exception
from common.svc_reg import svc_register
import log_pb2
from pg_constants import POSTGRES_TYPE


def main():
    while True:
        try:
            # initialize postgres database connection
            pg = PgHandler(dbname, username=pg_username, password=pg_password, host=pg_server)
            pg.create_schemas()
            pg.create_tables()
            log(POSTGRES_TYPE, log_pb2.INFO, "Postgres database has been created and available for connections")
            break
        except Exception:
            exception(msg="Unexpected error happens when initializing postgres, retrying.")
            time.sleep(10)


if __name__ == "__main__":
    main()
