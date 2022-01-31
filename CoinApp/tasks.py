import logging

import requests
from celery import Celery
from django.conf import settings
from django.utils.dateparse import parse_datetime

from CoinApp.models import ExchangeRate

settings.configure()

app = Celery("tasks", broker=settings.TASK_QUEUE_URL)
app.conf.result_backend = settings.TASK_RESULT_BACKEND

logger = logging.getLogger(__name__)


@app.task
def fetch_exchange_rate():
    from_currency = "BTC"
    to_currency = "USD"
    url = (
        f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
        f"&from_currency={from_currency}&to_currency={to_currency}"
        f"&apikey={settings.ALPHAVANTAGE_API_KEY}"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    rate = ExchangeRate()
    rate.rate = data["5. Exchange Rate"]
    rate.alphavantage_timestamp = parse_datetime(data["6. Last Refreshed"])
    # data["7. Time Zone"]
    rate.bid_price = data["8. Bid Price"]
    rate.ask_price = data["9. Ask Price"]
    rate.save()
    logger.info(
        f"Fetched new exchange rate for {rate.from_currency}/{rate.to_currency}: {rate.rate}"
    )
