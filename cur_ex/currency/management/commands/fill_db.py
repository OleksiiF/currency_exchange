from django.core.management.base import BaseCommand

from  cur_ex.currency.models import Currency, CurrencyHistory


class Command(BaseCommand):
    help = 'Fills the database with the main currency pairs and some history.'

    def handle(self, *args, **options):
        cur_codes = [
            'AUD', 'USD', 'EUR', 'CAD',
            'NZD', 'CHF', 'TRY', 'EUR',
            'HKD', 'MXN', 'BGN', 'GBP'
        ]

        for name in cur_codes:
            Currency.objects.get_or_create(name=name)

        histories = [
            {
                'rate_bid': 24.45,
                'rate_ask': 24.95,
                'date': '2019-12-30',
                'currency': 'USD'
            },
            {
                'rate_bid': 24.15,
                'rate_ask': 24.55,
                'date': '2020-01-03',
                'currency': 'USD'
            },
            {
                'rate_bid': 24.15,
                'rate_ask': 24.45,
                'date': '2020-01-15',
                'currency': 'USD'
            },
            {
                'rate_bid': 24.15,
                'rate_ask': 24.45,
                'date': '2020-01-18',
                'currency': 'USD'
            },
            {
                'rate_bid': 27.15,
                'rate_ask': 28.45,
                'date': '2020-01-15',
                'currency': 'EUR'
            },
            {
                'rate_bid': 28.15,
                'rate_ask': 29.05,
                'date': '2020-01-20',
                'currency': 'EUR'
            }
        ]

        for history in histories:
            history['currency'] = Currency.objects.get(
                name=history['currency']
            )
            CurrencyHistory.objects.get_or_create(**history)
