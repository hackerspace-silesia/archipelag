from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from archipelag.ngo.models import NgoUser
from archipelag.market.models import Market
from rest_framework_jwt import utils, views
from django.forms.models import model_to_dict

class BaseTestCase(TestCase):

    def setUp(self):
        self.email = 'jpueblo@example.com'
        self.username = 'jpueblo'
        self.password = 'password'
        user = User.objects.create_user(
            self.username, self.email, self.password)
        self.user = NgoUser.objects.create(
            user=user, organisation="org")

        self.data = {
            'username': self.username,
            'password': self.password
        }

class MarketTestCase(BaseTestCase):

    def setUp(self):
        super(MarketTestCase, self).setUp()

    def test_create_market_when_not_jwt(self):
        user = dict(title="123")
        client = APIClient().post('/api/market/', user, format='json')
        assert client.json()["detail"] == 'Authentication credentials were not provided.'

    @patch('archipelag.market.views.MarketList.permission_classes')
    def test_create_market_when_correct(self, authentication):
        # orig_token = self.get_token()
        authentication.return_value = None
        # Now try to get a refreshed token
        # response = client.post('/auth-token-verify/', ,
        #                        format='json')
        # user = dict(title="123")
        expected_market = Market.objects.create(owner=self.user, title="treerr", hashtag="#ff")
        client = APIClient().get('/api/market/', format="json")
        print(client.json()[0])
        print(model_to_dict(expected_market))
        assert client.json()[0]["title"] ==Market.value_list('title')

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