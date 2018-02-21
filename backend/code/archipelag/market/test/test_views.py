from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from django.forms.models import model_to_dict
from pytest import fixture

from archipelag.ngo.models import NgoUser
from archipelag.market.models import Market


class BaseTestCase(TestCase):

    def setUp(self):
        self.email = 'jpueblo@example.com'
        self.username = 'jpueblo'
        self.password = 'password'
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.ngo = NgoUser.objects.create(
            user=self.user, organisation="org", coins=10)

        self.data = {
            'username': self.username,
            'password': self.password
        }

class MarketTestCase(BaseTestCase):

    def setUp(self):
        super(MarketTestCase, self).setUp()

    # @fixture
    # def mock_required_authenticate(self):
    #     with  as mock:
    #         mock.return_value = None
    #         return mock

    def test_create_market_when_not_jwt(self):
        user = dict(title="123")
        client = APIClient().post('/api/market/', user, format='json')
        assert client.json()["detail"] == 'Authentication credentials were not provided.'

    @patch('archipelag.market.views.MarketList.permission_classes', [])
    def test_get_market_ordered_by_newest(self):
        expected_market = Market.objects.create(owner=self.ngo, title="1", hashtag="#1")
        expected_market2 = Market.objects.create(owner=self.ngo, title="2", hashtag="#2")
        market_list = APIClient().get('/api/market/', format="json").json()

        oldest_market = model_to_dict(expected_market)
        newest_market = model_to_dict(expected_market2)
        assert market_list[0]["title"] ==newest_market['title']
        assert market_list[1]["title"] ==oldest_market['title']

    # @patch('archipelag.market.views.MarketList.permission_classes', [])
    def test_create_market(self):
        client = APIClient()
        yolo = client.force_authenticate(self.user)
        print(yolo)
        market = {'body': {'title': 'jjj', 'hashtag': 'hh', 'date_starting': '2018-02-20 23:50', 'date_ending': '2018-02-20 23:50'}}

        market_list = client.post('/api/market/', market, format="json").json()

        assert market_list == {'success': {'market_id': 1}}

# class VerifyJSONWebTokenTestsSymmetric(TokenTestCase):
#
#     def test_verify_jwt(self):
#         """
#         Test that a valid, non-expired token will return a 200 response
#         and itself when passed to the validation endpoint.
#         """
#         client = APIClient()
#         response = client.post('/api/ngo/login/', self.data,
#                                format='json')
#
#
#         assert response.data == 1
#
#
# class MarketViewsTest():
#
#     def test_create_market(self):
#         pass