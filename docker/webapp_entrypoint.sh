#!/bin/bash

set -euxo pipefail

sleep 6 # give postgres time to start

poetry run python3 manage.py migrate
poetry run python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('test_user', 'test@example.com', 'foobar2022')"

pwd

poetry run gunicorn -b 0.0.0.0:8000 -w 4 coins.wsgi:application
