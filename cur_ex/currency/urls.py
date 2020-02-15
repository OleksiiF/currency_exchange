from django.urls import path

from cur_ex.currency.views import CurrentCurrency, OneCurrencyHistory

urlpatterns = [
    path('currency/<code>', OneCurrencyHistory.as_view(), name='currency_history'),
    path('current', CurrentCurrency.as_view(), name='current'),
]
