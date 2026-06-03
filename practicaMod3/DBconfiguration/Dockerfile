#Usar la imagen oficial de postgreSQL
FROM postgres:latest
#Copiar el script de sql al directorio de inicialización de PostgreSQL.
#(se ejecutan automaticamente al crear el volumen de datos por primera vez)
#El prefijo de 01_ y 02_ es el orden de ejecución
COPY init.sql /docker-entrypoint-initdb.d/01_init.sql
COPY save_data.sql /docker-entrypoint-initdb.d/02_save_data.sql
