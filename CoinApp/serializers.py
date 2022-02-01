from rest_framework.serializers import ModelSerializer

from CoinApp.models import ExchangeRate


class ExchangeRateSerializer(ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = [
            "from_currency",
            "to_currency",
            "rate",
            "timestamp",
            "alphavantage_timestamp",
            "bid_price",
            "ask_price",
        ]
