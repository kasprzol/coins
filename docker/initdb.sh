#!/bin/bash

set -euxo pipefail

echo "creating db & user"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE ${coins_db_name};
    CREATE USER ${coins_db_user} WITH PASSWORD '$coins_db_password';
    GRANT ALL PRIVILEGES ON DATABASE ${coins_db_name} TO ${coins_db_user};
    ALTER USER ${coins_db_user} CREATEDB;
EOSQL

echo "db and user created"
