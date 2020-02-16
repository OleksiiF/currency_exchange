import datetime

from django.db import IntegrityError
from django.test import TestCase, Client

from cur_ex.currency.models import CurrencyHistory, Currency


class CurrencyModelTestCase(TestCase):

    def test_add_data(self):
        names = ['USD', 'EUR']

        currency1 = Currency.objects.create(name=names[0])
        currency2 = Currency.objects.create(name=names[1])

        self.assertEqual(len(names), Currency.objects.all().count())
        self.assertEqual(names[1], currency2.name)

    def test_unique_name(self):
        currency = "USD"
        Currency.objects.create(name=currency)

        with self.assertRaises(IntegrityError):
            Currency.objects.create(name=currency)


class CurrencyHistoryModelTestCase(TestCase):

    def setUp(self):
        Currency.objects.create(name="USD")

    def test_add_rates(self):
        rate1 = {
            'rate_bid': 256.5,
            'rate_ask': 565.56,
            'date': '2020-02-16',
            'currency': Currency.objects.all().last()
        }
        rate2 = {
            'rate_bid': 300.01,
            'rate_ask': 400.02,
            'date': '2020-02-20',
            'currency': Currency.objects.all().last()
        }

        rates = [rate1, rate2]

        for rate in rates:
            CurrencyHistory.objects.create(**rate)

        self.assertEqual(len(rates), CurrencyHistory.objects.all().count())

        currency_history = CurrencyHistory.objects.filter(
            date=rate1["date"],
            currency=Currency.objects.all().last()
        ).last()

        self.assertEqual(
            rate1["currency"].name, Currency.objects.all().last().name
        )
        self.assertEqual(rate1["rate_bid"], currency_history.rate_bid)


class AddRateConcreteDateTestCase(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        Currency.objects.create(name="USD")

    def test_add_currency(self):
        rate = {
            'rate_bid': 256.5,
            'rate_ask': 565.56,
            'date': '2020-02-16',
            'currency': Currency.objects.all().last().id
        }
        response = self.client.post(
            "/add-new-rate", rate, follow=True
        )

        cur_history = CurrencyHistory.objects.filter(
            date=rate.get("date"),
            currency=Currency.objects.all().last()
        ).last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(rate["rate_bid"], cur_history.rate_bid)
        self.assertEqual(rate["rate_ask"], cur_history.rate_ask)
        self.assertEqual(rate["date"], str(cur_history.date))


class AddRateNowDateTestCase(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.now_date = datetime.datetime.now().date()
        Currency.objects.create(name="USD")

    def test_add_currency(self):
        rate = {
            'rate_bid': 256.5,
            'rate_ask': 565.56,
            'date': self.now_date,
            'currency': Currency.objects.all().last().id
        }
        response = self.client.post(
            "/add-new-rate", rate, follow=True
        )

        cur_history = CurrencyHistory.objects.filter(
            date=rate.get("date"),
            currency=Currency.objects.all().last()
        ).last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(rate["rate_bid"], cur_history.rate_bid)
        self.assertEqual(rate["rate_ask"], cur_history.rate_ask)
        self.assertEqual(rate["date"], self.now_date)


class DeleteRateTestCase(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.date_for_test = '2020-02-20'
        self.currency = 'USD'
        Currency.objects.create(name=self.currency)
        rate1 = {
            'rate_bid': 256.5,
            'rate_ask': 565.56,
            'date': '2020-02-16',
            'currency': Currency.objects.all().last()
        }
        rate2 = {
            'rate_bid': 300.01,
            'rate_ask': 400.02,
            'date': self.date_for_test,
            'currency': Currency.objects.all().last()
        }

        rates = [rate1, rate2]

        for rate in rates:
            CurrencyHistory.objects.create(**rate)


    def test_delete_rate(self):
        total_obj_before = CurrencyHistory.objects.all().count()
        client_for_destroy = CurrencyHistory.objects.get(
            date=self.date_for_test,
            currency=Currency.objects.get(name=self.currency)
        )

        response = self.client.get(
            f"/delete-rate/{client_for_destroy.id}", follow=True
        )

        total_obj_after = CurrencyHistory.objects.all().count()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(total_obj_before, total_obj_after)
