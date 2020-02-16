import datetime

from django import forms

from cur_ex.currency.models import CurrencyHistory


class RatesAddForm(forms.ModelForm):

    class Meta:
        model = CurrencyHistory
        fields = ['rate_bid', 'rate_ask', 'currency', 'date']

    def __init__(self, *args, **kwargs):
        super(RatesAddForm, self).__init__(*args, **kwargs)
        # add tips for user
        self.fields['date'].help_text = 'YYYY-MM-DD'

    def clean(self):
        date = self.cleaned_data['date']
        currency = self.cleaned_data['currency']

        if date > datetime.datetime.now().date():
            raise forms.ValidationError(
                'Date cannot be greater then current date.'
            )

        elif date < datetime.date(1900, 1, 1):
            raise forms.ValidationError(
                'Date cannot be less then 1900.'
            )

        elif CurrencyHistory.objects.filter(
            date=date,
            currency=currency
        ).exists():
            raise forms.ValidationError(
                'Record for this currency and date already exists.'
            )
