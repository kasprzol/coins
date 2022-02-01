from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from CoinApp.models import ExchangeRate
from CoinApp.serializers import ExchangeRateSerializer
from CoinApp.tasks import fetch_exchange_rate


class ExchangeRateViewSet(ModelViewSet):
    queryset = ExchangeRate.objects.order_by("-timestamp")
    serializer_class = ExchangeRateSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Trigger fetching new quotes."""
        fetch_exchange_rate.delay()
        return Response(status=HTTPStatus.ACCEPTED)

    def get_serializer_class(self):
        """Empty serializer for POST requests"""
        if self.action == "create":
            return Serializer()
        return super().get_serializer_class()
