from django.core.validators import MinLengthValidator
from django.db import models


class ExchangeRate(models.Model):
    from_currency = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        validators=(MinLengthValidator(limit_value=2),),
    )
    to_currency = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        validators=(MinLengthValidator(limit_value=2),),
    )
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    alphavantage_timestamp = models.DateTimeField(null=False, blank=False)
    rate = models.FloatField(null=False, blank=False)
    bid_price = models.FloatField(null=False, blank=False)
    ask_price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f"{self.from_currency}/{self.to_currency}: {self.rate}"
