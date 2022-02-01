import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils.dateparse import parse_datetime

from CoinApp.models import ExchangeRate

logger = get_task_logger(__name__)


class ApiLimitReached(RuntimeError):
    pass


@shared_task
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
    logger.warning(f"Received response: {data}")

    if "Note" in data:
        raise ApiLimitReached(data["Note"])
    rate = ExchangeRate()
    data = data["Realtime Currency Exchange Rate"]
    rate.from_currency = data["1. From_Currency Code"]
    rate.to_currency = data["3. To_Currency Code"]
    rate.rate = float(data["5. Exchange Rate"])
    rate.alphavantage_timestamp = parse_datetime(data["6. Last Refreshed"])
    # data["7. Time Zone"]
    rate.bid_price = float(data["8. Bid Price"])
    rate.ask_price = float(data["9. Ask Price"])
    rate.save()
    logger.info(
        f"Fetched new exchange rate for {rate.from_currency}/{rate.to_currency}: {rate.rate}"
    )
