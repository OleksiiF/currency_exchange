import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from cur_ex.currency.forms import RatesAddForm
from cur_ex.currency.models import CurrencyHistory, Currency


class CurrentCurrency(View):
    template_name = "current_rates.html"

    def get(self, request, *args, **kwargs):
        rates = Currency.objects.all()
        data = [
            CurrencyHistory.objects.filter(
                currency=rate_name
            ).order_by('date').last()
            for rate_name in rates
            if CurrencyHistory.objects.filter(currency=rate_name).exists()
        ]

        for value in data:
            value.set_date_end(datetime.datetime.now().date())

        return render(
            self.request,
            self.template_name,
            {'rates': data}
        )


class OneCurrencyHistory(View):
    template_name = 'history_currency.html'

    def get(self, request, *args, **kwargs):
        data = CurrencyHistory.objects.filter(
            currency__name=kwargs['code']
        ).order_by('date')
        for index, value in enumerate(data):
            try:
                value.set_date_end(
                    data[index+1].date - datetime.timedelta(days=1)
                )

            except IndexError:
                value.set_date_end(datetime.datetime.now().date())

        return render(
            self.request,
            self.template_name,
            {"history": data}
        )


class AddRateView(View):
    template_name = 'add_new_rate.html'

    def get(self, request, *args, **kwargs):
        form = RatesAddForm(request.GET or None)
        context = {'form': form}

        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RatesAddForm(request.POST or None)

        if form.is_valid():
            CurrencyHistory.objects.create(**form.cleaned_data)

            return HttpResponseRedirect(
                f'currency/{form.cleaned_data["currency"]}'
            )

        context = {'form': form}

        return render(self.request, self.template_name, context)


class DeleteRateView(View):

    def get(self, request, *args, **kwargs):
        CurrencyHistory.objects.get(id=kwargs['id']).delete()

        return HttpResponseRedirect('/')
