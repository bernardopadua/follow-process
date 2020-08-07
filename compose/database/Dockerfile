FROM postgres:latest

RUN mkdir -p /var/lib/postgresql \
 && mkdir -p /var/lib/postgresql/ndata \
 && chown postgres:postgres /var/lib/postgresql \
 && chown postgres:postgres /var/lib/postgresql/ndata

ENV POSTGRES_PASSWORD=passdatabase
ENV PGDATA=/var/lib/postgresql/ndata

EXPOSE 5432