from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from uuid import uuid4

from archipelag.ngo.models import NgoUser
from archipelag.market.models import Market
from archipelag.market.models import Image
from io import BytesIO
from unittest.mock import MagicMock

class BaseTestCase(TransactionTestCase):

    def setUp(self):
        email = 'jpueblo@example.com'
        username = 'jpueblo'
        password = 'password'
        self.user = User.objects.create_user(
            username, email, password)
        self.ngo = NgoUser.objects.create(
            user=self.user, organisation="org", coins=10)


class ImageTestCase(BaseTestCase):
    reset_sequences = True

    def setUp(self):
        super(ImageTestCase, self).setUp()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_image_when_not_jwt(self):
        client = APIClient().post('/api/images/', format='json')
        assert client.json()["detail"] == 'Authentication credentials were not provided.'

    @patch('archipelag.market.views.MarketImageSerializer')
    def test_create_image_when_wrong_market_id(self, serializer):

        data = dict(market_id=uuid4())
        error = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data)
        assert error.json()["error"] == 'Prośba o dodanie obrazka do nieistniejącego marketu'

    @patch('archipelag.market.views.MarketImageSerializer')
    def test_create_image_when_id_is_not_uuid(self, serializer):
        data = dict(market_id='212')
        error = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data)
        assert error.json()["error"] == dict(market_id='badly formed hexadecimal UUID string')


    def test_create_image_when_when_missing_file(self):
        data = dict(market_id=uuid4())

        error = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data,)
        assert error.json()["error"] == dict(image_path=['This field may not be null.'])

    def test_create_image_when_when_missing_id_and_file(self):
        data = dict(file=uuid4())

        error = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data,)
        assert error.json()["error"] == dict(market_id=['This field may not be null.'],
                                             image_path=['This field may not be null.'])

    def test_create_image_when_when_not_valid(self):
        data = dict(market_id=uuid4(), file="")

        error = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data,)
        assert error.json()["error"] == dict(image_path=['This field may not be null.'])

    @patch('archipelag.market.views.MarketImageSerializer')
    @patch('archipelag.market.views.Image.objects.create')
    def test_create_image_correctly(self, mock_create, mock_validator):
        images_market = Market.objects.create(owner=self.ngo, title="1", hashtag="#1")
        data = dict(market_id=images_market.id)

        data['file'] = (BytesIO(b"abcdef"), "file.jpg")
        market_list = self.client.post('/api/images/',
                                       data=data).json()
        assert market_list == dict(success='Przesłano poprawnie')

    @patch('archipelag.market.views.Image.objects.filter')
    @patch('archipelag.market.views.MarketImageSerializer')
    def test_create_image_when_too_many_images(self, serializer, images):
        expected_market = Market.objects.create(owner=self.ngo, title="1", hashtag="#1")
        images.return_value.count.return_value = 4
        Image.objects.filter().count()
        data = dict(market_id=expected_market.id)

        data['file'] = (BytesIO(b"abcdef"), "file.jpg")
        market_list = self.client.post('/api/images/',
                                       data=data,).json()
        assert market_list == dict(error='Do marketu już dodano 4 obrazki.')
