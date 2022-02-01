from http import HTTPStatus

from django.http import Http404
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
        """Based on the specification the endpoint - return one rate instead of
        list of all rates"""
        queryset = self.filter_queryset(self.get_queryset())

        obj = queryset.first()
        if not obj:
            raise Http404
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    # disallow any other GET endpoints (e.g. /api/v1/quotes/3/)
    def retrieve(self, request, *args, **kwargs):
        raise Http404

    def create(self, request, *args, **kwargs):
        """Trigger fetching new quotes."""
        if request.data:
            return Response(
                {"error": "Wasn't expecting any request body."},
                status=HTTPStatus.BAD_REQUEST,
            )
        fetch_exchange_rate.delay()
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses
        # 202 Accepted
        #
        # The request has been received but not yet acted upon. It is
        # noncommittal, since there is no way in HTTP to later send an
        # asynchronous response indicating the outcome of the request. It is
        # intended for cases where another process or server handles the
        # request, or for batch processing.
        return Response(status=HTTPStatus.ACCEPTED)

    def get_serializer_class(self):
        """Empty serializer for POST requests"""
        if self.action == "create":
            return Serializer()
        return super().get_serializer_class()
