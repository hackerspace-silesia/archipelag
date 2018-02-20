from calendar import timegm

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from archipelag.market.views import MarketList
from archipelag.market.models import Market
from archipelag.ngo.models import NgoUser
from rest_framework_jwt import utils, views


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


class TokenTestCase(BaseTestCase):
    """
    Handlers for getting tokens from the API, or creating arbitrary ones.
    """

    def setUp(self):
        super(TokenTestCase, self).setUp()

    def get_token(self):
        client = APIClient()
        response = client.post('/api/ngo/token-verify/', self.data, format='json')
        return response.data['token']

    def create_token(self, user, exp=None, orig_iat=None):
        payload = utils.jwt_payload_handler(user)
        if exp:
            payload['exp'] = exp

        if orig_iat:
            payload['orig_iat'] = timegm(orig_iat.utctimetuple())

        token = utils.jwt_encode_handler(payload)
        return token



class MarketTestCase(TokenTestCase):

    def setUp(self):
        super(MarketTestCase, self).setUp()

    # def setUp(self):
    #     pass
        # user = User.objects.create_user(username='testUser', password="1234")
        # ngo = NgoUser.objects.create(user=user, organisation="organisation1")
        # Market.objects.create(owner=ngo, title="lion", hashtag="#roar")


    def test_create_market_when_not_jwt(self):
        user = dict(title="123")
        client = APIClient().post('/api/market/', user, format='json')
        assert client.json()["detail"] == 'Authentication credentials were not provided.'

    def test_create_market_when_correct(self):
        orig_token = self.get_token()

        # Now try to get a refreshed token
        # response = client.post('/auth-token-verify/', ,
        #                        format='json')
        # user = dict(title="123")
        client = APIClient().post('/api/market/', {'JWT': orig_token}, format='json')
        assert client.json() == 'Authentication credentials were not provided.'

class VerifyJSONWebTokenTestsSymmetric(TokenTestCase):

    def test_verify_jwt(self):
        """
        Test that a valid, non-expired token will return a 200 response
        and itself when passed to the validation endpoint.
        """
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/api/ngo/login/', self.data,
                               format='json')


        assert response.data == 1


class MarketViewsTest():

    def test_create_market(self):
        pass