FROM postgis/postgis:15-3.3

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=czas_kobiet
ENV POSTGRES_DB=mapa

# Wrzucamy conf-y w miejsce, które Postgres zna
COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY pg_hba.conf /etc/postgresql/pg_hba.conf

EXPOSE 5432

