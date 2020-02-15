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
                'date_start': '2019-12-30',
                'date_end': '2020-02-02',
                'currency': 'USD'
            },
            {
                'rate_bid': 24.15,
                'rate_ask': 24.55,
                'date_start': '2020-01-03',
                'date_end': '2020-01-14',
                'currency': 'USD'
            },
            {
                'rate_bid': 24.15,
                'rate_ask': 24.45,
                'date_start': '2020-01-15',
                'date_end': '2020-01-17',
                'currency': 'USD'
            },
            {
                'rate_bid': 27.15,
                'rate_ask': 28.45,
                'date_start': '2020-01-15',
                'date_end': '2020-01-16',
                'currency': 'EUR'
            },
            {
                'rate_bid': 28.15,
                'rate_ask': 29.05,
                'date_start': '2020-01-17',
                'date_end': '2020-01-20',
                'currency': 'EUR'
            }
        ]

        for history in histories:
            history['currency'] = Currency.objects.get(
                name=history['currency']
            )
            CurrencyHistory.objects.get_or_create(**history)
