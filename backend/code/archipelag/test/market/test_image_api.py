from unittest.mock import patch
from uuid import uuid4

from rest_framework.test import APIClient

from archipelag.market.models import Market
from archipelag.test.base_test_case import BaseTestCase


class TestImage(BaseTestCase):

    def test_create_image_when_not_jwt(self):
        client = APIClient().post('/api/images/', format='json')
        assert client.json()["detail"] == 'Authentication credentials were not provided.'

    def test_create_image_when_wrong_market_id(self, auth_client):
        client, ngo = auth_client
        with open("test/market/socek.png", 'rb') as file:
            data = dict(market_id=uuid4(), file=file)
            response = client.post(
                '/api/images/',
                data,
                format='multipart',
            )
        assert response.json()["error"] == 'Prośba o dodanie obrazka do nieistniejącego marketu'
        assert response.status_code == 400

    def test_create_image_when_id_is_not_uuid(self, auth_client):
        client, ngo = auth_client
        with open("test/market/socek.png", 'rb') as file:
            data = dict(market_id='121212', file=file)
            response = client.post(
                '/api/images/',
                follow_redirects=True,
                data=data,
                format='multipart')
        assert response.json()["error"] == dict(market_id='badly formed hexadecimal UUID string')
        assert response.status_code == 400

    def test_create_image_when_when_missing_file(self, auth_client):
        client, ngo = auth_client
        data = dict(market_id=uuid4())

        response = client.post(
            '/api/images/',
            follow_redirects=True,
            data=data,
        )
        assert response.json()["error"] == dict(image_path=['This field may not be null.'])
        assert response.status_code == 400

    def test_create_image_when_when_missing_id_and_file(self, auth_client):
        client, ngo = auth_client
        data = dict(file=uuid4())

        response = client.post(
            '/api/images/',
            follow_redirects=True,
            data=data,
        )
        assert response.json()["error"] == dict(
            market_id=['This field may not be null.'],
            image_path=['This field may not be null.'])
        assert response.status_code == 400

    def test_create_image_when_when_not_valid(self, auth_client):
        client, ngo = auth_client
        data = dict(market_id=uuid4(), file="")

        response = client.post(
            '/api/images/',
            follow_redirects=True,
            data=data,
        )
        assert response.json()["error"] == dict(image_path=['This field may not be null.'])
        assert response.status_code == 400

    @patch('archipelag.market.views.Image.objects.create')
    def test_create_image_correctly(self, mock_create, auth_client):
        client, ngo = auth_client
        images_market = Market.objects.create(
            owner=ngo, title="1", hashtag="#1")

        with open("test/market/socek.png", 'rb') as file:
            data = dict(market_id=images_market.id, file=file)
            response = client.post(
                '/api/images/',
                data,
                format='multipart',
            )
        assert response.json() == dict(message='Przesłano poprawnie')
        assert response.status_code == 200

    @patch('archipelag.market.views.Image.objects.filter')
    def test_create_image_when_too_many_images(self, images, auth_client):
        client, ngo = auth_client
        expected_market = Market.objects.create(
            owner=ngo, title="1", hashtag="#1")
        images.return_value.count.return_value = 4

        with open("test/market/socek.png", 'rb') as file:
            data = dict(market_id=expected_market.id, file=file)
            response = client.post(
                '/api/images/',
                data,
                format='multipart',
            )
        assert response.json() == dict(error='Do marketu już dodano 4 obrazki.')
        assert response.status_code == 400
