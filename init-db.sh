#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
  SELECT 'CREATE DATABASE meeting_db'
  WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'meeting_db')\gexec
EOSQL
echo "Creating Kong database..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    CREATE DATABASE kong_db;
    GRANT ALL PRIVILEGES ON DATABASE kong_db TO user;
EOSQL
echo "Database created."
