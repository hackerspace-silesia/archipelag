from unittest.mock import patch
from uuid import uuid4
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from django.forms.models import model_to_dict
from unittest.mock import MagicMock

from archipelag.ngo.models import NgoUser
from archipelag.market.models import Market
from archipelag.market.models import Image
from io import BytesIO

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

    def test_create_image_when_wrong_market_id(self):

        data = {'market_id': uuid4()}
        error = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data,
                                 )

        assert error.json()["error"] == 'Prośba o dodanie obrazka do nieistniejącego marketu'

    @patch('archipelag.market.views.MarketImageSerializer')
    @patch('archipelag.market.views.Image.objects.create')
    def test_create_image_correctly(self,  create, validator,):
        validator.return_value.is_valid.return_value = MagicMock()
        expected_market = Market.objects.create(owner=self.ngo, title="1", hashtag="#1")
        print(Image.objects.filter().count())
        data = {'market_id':expected_market.id}

        data['file'] = (BytesIO(b"abcdef"), "file.jpg")
        market_list = self.client.post('/api/images/',
                                       data=data,).json()

        assert market_list == {'success': 'Przesłano poprawnie'}

    @patch('archipelag.market.views.Image.objects.filter')
    @patch('archipelag.market.views.Image.objects.create')
    def test_create_image_when_too_many_images(self,  create, images,):
        expected_market = Market.objects.create(owner=self.ngo, title="1", hashtag="#1")
        images.return_value.count.return_value = 4
        Image.objects.filter().count()
        data = {'market_id':expected_market.id}

        data['file'] = (BytesIO(b"abcdef"), "file.jpg")
        market_list = self.client.post('/api/images/',
                                       data=data,).json()

        assert market_list == {'error': 'Do marketu już dodano 4 obrazki.'}


