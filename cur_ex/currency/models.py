from django.db import models
from cur_ex.core.models import UUID

# Create your models here.
class Currency(UUID):
    name = models.CharField(max_length=3, null=False)


class CurrencyHistory(UUID):
    rates_bid = models.FloatField()
    rates_offer = models.FloatField()
    date_start = models.DateField()
    date_end = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)



