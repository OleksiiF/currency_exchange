from django.db import models
from cur_ex.core.models import UUID


class Currency(UUID):
    name = models.CharField(max_length=3, null=False, unique=True)


class CurrencyHistory(UUID):
    rate_bid = models.FloatField()
    rate_ask = models.FloatField()
    date_start = models.DateField()
    date_end = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
