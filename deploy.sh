#!/usr/bin/env bash

set -e
source env/bin/activate
python -m pip install -r requirements/production.txt
python manage.py migrate
python manage.py collectstatic
deactivate