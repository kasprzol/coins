import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coins.settings")

app = Celery("coins")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "fetch-new-rates-every-hour": {
        "task": "CoinApp.tasks.fetch_exchange_rate",
        "schedule": crontab(hour="*", minute="20"),
    },
}
