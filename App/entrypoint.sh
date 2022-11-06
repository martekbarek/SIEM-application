#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python speedy7/manage.py flush --no-input
python speedy7/manage.py makemigrations
python speedy7/manage.py migrate

exec "$@"