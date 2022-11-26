#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python speedy7/manage.py makemigrations
# fake migrations for already created tables
python speedy7/manage.py migrate --fake-initial
python speedy7/manage.py createsuperuser --no-input

exec "$@"