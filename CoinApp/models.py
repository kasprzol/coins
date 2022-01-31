from django.db import models


class ExchangeRate(models.Model):
    from_currency = models.CharField(max_length=200, null=False, blank=False)
    to_currency = models.CharField(max_length=200, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    rate = models.FloatField(null=False, blank=False)
