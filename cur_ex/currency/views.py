from django.shortcuts import render
from django.views.generic.base import View

from cur_ex.currency.models import CurrencyHistory, Currency


class CurrentCurrency(View):
    template_name = "current_rates.html"

    def get(self, request, *args, **kwargs):
        rates = Currency.objects.all()
        data = []

        for rate_name in rates:
            if CurrencyHistory.objects.filter(currency=rate_name).exists():
                data.append(
                    CurrencyHistory.objects.filter(currency=rate_name).order_by('date_end').last()
                )

        return render(
            self.request,
            self.template_name,
            {'rates': data}
        )


class OneCurrencyHistory(View):
    template_name = 'history_currency.html'

    def get(self, request, *args, **kwargs):
        data = CurrencyHistory.objects.filter(currency__name=kwargs['code'])

        return render(
            self.request,
            self.template_name,
            {"history": data}
        )
