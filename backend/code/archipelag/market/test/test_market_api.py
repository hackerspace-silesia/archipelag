from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from django.forms.models import model_to_dict
from pytest import fixture

from archipelag.ngo.models import NgoUser
from archipelag.market.models import Market


class BaseTestCase(TransactionTestCase):

    def setUp(self):
        email = 'jpueblo@example.com'
        username = 'jpueblo'
        password = 'password'
        self.user = User.objects.create_user(
            username, email, password)
        self.ngo = NgoUser.objects.create(
            user=self.user, organisation="org", coins=10)


class MarketTestCase(BaseTestCase):
    reset_sequences = True

    def setUp(self):
        super(MarketTestCase, self).setUp()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_market_when_not_jwt(self):
        client = APIClient().post('/api/market/', format='json')
        assert client.json()["detail"] == 'Authentication credentials were not provided.'


    @patch('archipelag.market.views.MarketList.permission_classes', [])
    def test_get_market_ordered_by_newest(self):
        # given
        expected_market = Market.objects.create(owner=self.ngo, title="1", hashtag="#1")
        expected_market2 = Market.objects.create(owner=self.ngo, title="2", hashtag="#2")
        # when
        market_list = APIClient().get('/api/market/', format="json").json()
        # then
        oldest_market = model_to_dict(expected_market)
        newest_market = model_to_dict(expected_market2)
        assert market_list[0]["title"] == newest_market['title']
        assert market_list[1]["title"] == oldest_market['title']

    def test_correct_create_market(self):
        market = {'body': {'title': 'jjj', 'hashtag': 'hh', 'date_starting': '2018-02-20 23:50', 'date_ending': '2018-02-20 23:50'}}
        market_list = self.client.post('/api/market/', market, format="json").json()

        assert "success" in market_list

    def test_create_market_when_user_hasnt_coins(self):
        self.ngo.coins = 0
        self.ngo.save()
        market = {'body': {'title': 'jjj'}}
        market_list = self.client.post('/api/market/', market, format="json").json()

        assert market_list == {"error": "Za mało punktów."}

    def test_create_market_when_missing_required_field(self):
        market = {'body': {}}
        market_list = self.client.post('/api/market/', market, format="json").json()

        assert market_list == {"error": {'title': ['This field is required.']}}

    def test_create_market_when_wrong_date(self):
        market = {'body': {'title': 'jjj', 'date_starting': 'yyu'}}
        market_list = self.client.post('/api/market/', market, format="json").json()

        assert market_list == {"error": {'date_starting': ['Datetime has wrong format. Use one of these formats '
                                         'instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].']}}

    def test_create_market_when_not_know_field(self):
        market = {'body': {'title': 'jjj', 'hashtag': 'hh','h': '2018-02-20 23:50'}}
        market_list = self.client.post('/api/market/', market, format="json").json()

        assert market_list == {"error": "'h' is an invalid keyword argument for this function"}
