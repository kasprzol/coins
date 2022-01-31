#!/bin/bash

set -euxo pipefail

sleep 10 # give postgres time to start

python3 manage.py migrate

pwd

gunicorn -w 4 coins.wsgi:application
