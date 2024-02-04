#!/bin/bash

python manage.py collectstatic --clear
cp -r /app/collected_static/. /backend_static/

gunicorn --bind 0.0.0.0:8010 survey.wsgi
