from rest_framework.routers import DefaultRouter

from CoinApp.viewsets import ExchangeRateViewSet

router = DefaultRouter()
router.register("quotes", ExchangeRateViewSet)
