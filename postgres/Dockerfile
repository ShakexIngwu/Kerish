ARG DOCKER_REGISTRY=192.168.7.20:5000
FROM $DOCKER_REGISTRY/helios:postgres_base
LABEL maintainer="https://heliosdata.com/yisun"

COPY postgres_consul.json /opt/helios/consul_services/
COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY pg_migrate /opt/helios/pg_migrate
COPY pg_utils /opt/helios/pg_utils
# Please only turn on next line for dev only, do not
# commit the code
# COPY test /opt/helios/test

COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s usr/local/bin/docker-entrypoint.sh / # backwards compat
ENTRYPOINT ["docker-entrypoint.sh"]
EXPOSE 5432
CMD ["postgres"]
