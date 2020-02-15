from django.contrib import admin

from cur_ex.currency.models import Currency, CurrencyHistory


admin.site.register(Currency)
admin.site.register(CurrencyHistory)
