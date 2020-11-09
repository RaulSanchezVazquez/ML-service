FROM mysql

MAINTAINER Luis Raul Sanchez Vazquez "luisraulsv@gmail.com"

ENV MYSQL_DATABASE rappi
ENV MYSQL_ROOT_PASSWORD rappi-secret

COPY ./sql_scripts/ /docker-entrypoint-initdb.d/

EXPOSE 3306
