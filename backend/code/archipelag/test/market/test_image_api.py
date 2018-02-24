from rest_framework.test import APIClient
from unittest.mock import patch
from uuid import uuid4

from archipelag.market.models import Market
from archipelag.market.models import Image
from io import BytesIO
from archipelag.test.base_test_case import BaseTestCase


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
        response = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data)
        assert response.json()["error"] == 'Prośba o dodanie obrazka do nieistniejącego marketu'
        assert response.status_code == 400

    @patch('archipelag.market.views.MarketImageSerializer')
    def test_create_image_when_id_is_not_uuid(self, serializer):
        data = dict(market_id='212')
        response = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data)
        assert response.json()["error"] == dict(market_id='badly formed hexadecimal UUID string')
        assert response.status_code == 400

    def test_create_image_when_when_missing_file(self):
        data = dict(market_id=uuid4())

        response = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data,)
        assert response.json()["error"] == dict(image_path=['This field may not be null.'])
        assert response.status_code == 400

    def test_create_image_when_when_missing_id_and_file(self):
        data = dict(file=uuid4())

        response = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data,)
        assert response.json()["error"] == dict(market_id=['This field may not be null.'],
                                             image_path=['This field may not be null.'])
        assert response.status_code == 400

    def test_create_image_when_when_not_valid(self):
        data = dict(market_id=uuid4(), file="")

        response = self.client.post('/api/images/',
                                 follow_redirects=True,
                                 data=data,)
        assert response.json()["error"] == dict(image_path=['This field may not be null.'])
        assert response.status_code == 400

    @patch('archipelag.market.views.MarketImageSerializer')
    @patch('archipelag.market.views.Image.objects.create')
    def test_create_image_correctly(self, mock_create, mock_validator):
        images_market = Market.objects.create(owner=self.ngo, title="1", hashtag="#1")
        data = dict(market_id=images_market.id)

        data['file'] = (BytesIO(b"abcdef"), "file.jpg")
        response = self.client.post('/api/images/',
                                       data=data)
        assert response.json() == dict(success='Przesłano poprawnie')
        assert response.status_code == 200

    @patch('archipelag.market.views.Image.objects.filter')
    @patch('archipelag.market.views.MarketImageSerializer')
    def test_create_image_when_too_many_images(self, serializer, images):
        expected_market = Market.objects.create(owner=self.ngo, title="1", hashtag="#1")
        images.return_value.count.return_value = 4
        Image.objects.filter().count()
        data = dict(market_id=expected_market.id)

        data['file'] = (BytesIO(b"abcdef"), "file.jpg")
        response = self.client.post('/api/images/',
                                       data=data,)
        assert response.json() == dict(error='Do marketu już dodano 4 obrazki.')
        assert response.status_code == 400
