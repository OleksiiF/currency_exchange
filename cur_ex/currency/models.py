from django.db import models
from cur_ex.core.models import UUID


class Currency(UUID):
    name = models.CharField(max_length=3, null=False, unique=True)

    def __str__(self):
        return self.name


class CurrencyHistory(UUID):
    rate_bid = models.FloatField()
    rate_ask = models.FloatField()
    date = models.DateField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def set_date_end(self, value):
        """
        Uses on backend for creating intervals.
        """
        self.date_end = value

    def get_date_end(self):
        """
        Uses on template for rendering intervals.
        """
        return self.date_end
