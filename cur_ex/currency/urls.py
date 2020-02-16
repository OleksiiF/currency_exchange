from django.urls import path

from cur_ex.currency.views import CurrentCurrency, OneCurrencyHistory, AddRateView, DeleteRateView


urlpatterns = [
    path('currency/<code>', OneCurrencyHistory.as_view(), name='currency_history'),
    path('', CurrentCurrency.as_view(), name='current'),
    path('add-new-rate', AddRateView.as_view(), name='add_new_rate'),
    path('delete-rate/<id>', DeleteRateView.as_view(), name='delete_rate'),
]
