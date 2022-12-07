#!/bin/bash

python speedy7/manage.py makemigrations
python speedy7/manage.py migrate --fake-initial
python speedy7/manage.py createsuperuser --no-input
python speedy7/manage.py collectstatic --no-input --clear

exec "$@"