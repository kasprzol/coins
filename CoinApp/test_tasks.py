import unittest
from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from CoinApp.models import ExchangeRate
from CoinApp.tasks import ApiLimitReached, InvalidApiKey, fetch_exchange_rate


@override_settings(ALPHAVANTAGE_API_KEY="qwerty")
class Test(TestCase):
    @patch("CoinApp.tasks.requests")
    def test_fetch_exchange_rate(self, requests_mock):
        mock_response = Mock()
        btc = "BTC"
        usd = "USD"
        exchange_rate = "38495.21000000"
        mock_response.json.return_value = {
            "Realtime Currency Exchange Rate": {
                "1. From_Currency Code": btc,
                "2. From_Currency Name": "Bitcoin",
                "3. To_Currency Code": usd,
                "4. To_Currency Name": "United States Dollar",
                "5. Exchange Rate": exchange_rate,
                "6. Last Refreshed": "2022-01-31 23:58:02",
                "7. Time Zone": "UTC",
                "8. Bid Price": "38495.20000000",
                "9. Ask Price": "38495.21000000",
            }
        }
        requests_mock.get.return_value = mock_response
        self.assertEqual(ExchangeRate.objects.count(), 0)
        fetch_exchange_rate()
        self.assertEqual(ExchangeRate.objects.count(), 1)
        rate: ExchangeRate = ExchangeRate.objects.first()
        self.assertEqual(rate.from_currency, btc)
        self.assertEqual(rate.to_currency, usd)
        self.assertAlmostEqual(rate.rate, float(exchange_rate))

    @patch("CoinApp.tasks.requests")
    def test_fetch_exchange_rate_api_key_invalid(self, requests_mock):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Error Message": "the parameter apikey is invalid or missing. "
            "Please claim your free API key on "
            "(https://www.alphavantage.co/support/#api-key). "
            "It should take less than 20 seconds."
        }
        requests_mock.get.return_value = mock_response
        self.assertEqual(ExchangeRate.objects.count(), 0)
        self.assertRaises(InvalidApiKey, fetch_exchange_rate)
        self.assertEqual(ExchangeRate.objects.count(), 0)

    @patch("CoinApp.tasks.requests")
    def test_fetch_exchange_rate_api_limit_exceeded(self, requests_mock):
        mock_response = Mock()
        mock_response.json.return_value = {"Note": "api limit exceeded"}
        requests_mock.get.return_value = mock_response
        self.assertEqual(ExchangeRate.objects.count(), 0)
        self.assertRaises(ApiLimitReached, fetch_exchange_rate)
        self.assertEqual(ExchangeRate.objects.count(), 0)


if __name__ == "__main__":
    unittest.main()
