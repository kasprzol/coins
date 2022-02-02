import datetime
import json
from http import HTTPStatus

from django.test import Client, TestCase, override_settings
from rest_framework_api_key.models import APIKey

from CoinApp.models import ExchangeRate


@override_settings(ALPHAVANTAGE_API_KEY="qwerty")
class TestApi(TestCase):
    def setUp(self) -> None:
        api_key_obj, key_value = APIKey.objects.create_key(name="api_key_for_test")
        self.api_key = key_value
        self.rate = ExchangeRate.objects.create(
            from_currency="BTC",
            to_currency="USD",
            rate=3.14,
            ask_price=1.23,
            bid_price=2.89,
            alphavantage_timestamp=datetime.datetime.now(),
            timestamp=datetime.datetime.now(),
        )

    def test_get_without_apikey(self):
        client = Client()
        response = client.get("/api/v1/quotes/")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_with_apikey(self):
        client = Client(HTTP_AUTHORIZATION=f"Api-Key {self.api_key}")
        response = client.get(
            "/api/v1/quotes/",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        rate_from_api = json.loads(response.content)
        self.assertEqual(rate_from_api["from_currency"], self.rate.from_currency)
        self.assertEqual(rate_from_api["to_currency"], self.rate.to_currency)
        self.assertEqual(rate_from_api["rate"], self.rate.rate)
        self.assertEqual(rate_from_api["bid_price"], self.rate.bid_price)
        self.assertEqual(rate_from_api["ask_price"], self.rate.ask_price)

    def test_post_without_apikey(self):
        client = Client()
        response = client.post("/api/v1/quotes/")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    # TODO: find a way to patch the task so that it doesn't communicate with
    #  queue/celery workers. Patch should work as tests and test server
    #  appear to be running in the same process. But it fails.
    #
    # @patch("CoinApp.tasks.fetch_exchange_rate")
    # def test_post_with_apikey(self, task_mock):
    #     client = Client(HTTP_AUTHORIZATION=f"Api-Key {self.api_key}")
    #     response = client.post("/api/v1/quotes/")
    #     self.assertEqual(response.status_code, HTTPStatus.ACCEPTED)
    #     self.assertTrue(task_mock.delay.calls)
