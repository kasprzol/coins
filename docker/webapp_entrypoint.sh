#!/bin/bash

set -euxo pipefail

sleep 6 # give postgres time to start

poetry run python3 manage.py migrate

pwd

poetry run gunicorn -b 0.0.0.0:8000 -w 4 coins.wsgi:application
