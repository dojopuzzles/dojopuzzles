#!/bin/sh

printenv | grep -v "no_proxy" >> /etc/environment

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn --workers=2 --bind=0.0.0.0:8100 dojopuzzles.wsgi:application
