from unittest.mock import patch
from uuid import uuid4

from pytest import fixture
from rest_framework.test import APIClient

from archipelag.market.models import Market
from archipelag.market.models import Image
from archipelag.test.base_test_case import BaseTestCase


class TestImage(BaseTestCase):

    def test_create_image_when_not_jwt(self):
        client = APIClient().post('/api/images/', format='json')
        assert client.json()["detail"] == 'Nie podano danych uwierzytelniających.'

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
        assert response.json()["error"] == dict(market_id=['"121212" nie jest poprawnym UUID.'])
        assert response.status_code == 400

    def test_create_image_when_when_missing_file(self, auth_client):
        client, ngo = auth_client
        data = dict(market_id=uuid4())

        response = client.post(
            '/api/images/',
            follow_redirects=True,
            data=data,
        )
        assert response.json()["error"] == dict(image_path=['Pole nie może mieć wartości null.'])
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
            market_id=['Pole nie może mieć wartości null.'],
            image_path=['Pole nie może mieć wartości null.'])
        assert response.status_code == 400

    def test_create_image_when_when_not_valid(self, auth_client):
        client, ngo = auth_client
        data = dict(market_id=uuid4(), file="")

        response = client.post(
            '/api/images/',
            follow_redirects=True,
            data=data,
        )
        assert response.json()["error"] == dict(image_path=['Pole nie może mieć wartości null.'])
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


class TestGetImage(BaseTestCase):

    @fixture
    def market_with_image(self, user_with_ngo):
        user, ngo = user_with_ngo
        market = Market.objects.create(owner=ngo, title="1", hashtag="#1")
        image = Image.objects.create(market=market, image_path="yolo")
        return market, image

    def test_get_images_correctly_return_correct_status(self, auth_client):
        client, ngo = auth_client
        market = Market.objects.create(
            owner=ngo, title="1", hashtag="#1")
        Image.objects.create(market=market, image_path="yolo")
        response = client.get('/api/images/?market_id={}'.format(market.id),)
        assert response.status_code == 200

    def test_get_images_correctly_return_correct_data_with_one_image(self, auth_client, market_with_image):
        client, ngo = auth_client
        market, expected_image = market_with_image
        response = client.get('/api/images/?market_id={}'.format(market.id),)
        returned_images = response.json()

        assert len(returned_images) == 1
        assert returned_images[0]["id"] == expected_image.id
        assert returned_images[0]["image_path"] == "/media/{}"\
                                                   .format(str(expected_image.image_path))
        assert returned_images[0]["market_id"] == str(expected_image.market_id)

    def test_get_images_correctly_return_data_with_two_images(self, auth_client, market_with_image):
        client, ngo = auth_client
        market, expected_image = market_with_image
        expected_second_image = Image.objects.create(market=market, image_path="yolo")
        response = client.get('/api/images/?market_id={}'.format(market.id),)
        returned_images = response.json()

        assert len(returned_images) == 2
        assert returned_images[1]["id"] == expected_second_image.id
        assert returned_images[1]["image_path"] == "/media/{}".format(str(expected_image.image_path))
        assert returned_images[1]["market_id"] == str(expected_image.market_id)

    def test_get_images_when_missing_market_id(self, auth_client):
        client, ngo = auth_client
        response = client.get('/api/images/')
        assert response.status_code == 422
        assert response.json() == dict(error="Brakuje marketu dla którego można by pobrać obrazki")

    def test_get_images_correctly_return_images_only_from_one_market(self, auth_client, market_with_image):
        client, ngo = auth_client
        market, expected_image = market_with_image

        market2 = Market.objects.create(owner=ngo, title="life is life", hashtag="#1")
        image2 = Image.objects.create(market=market2, image_path="yolo")

        response = client.get('/api/images/?market_id={}'.format(market.id))
        returned_images = response.json()
        assert len(returned_images) == 1

    def test_get_images_when_not_correct_market_uuid(self, auth_client):
        client, ngo = auth_client
        response = client.get('/api/images/?market_id={}'.format("444444"))
        assert response.status_code == 422
        assert response.json() == dict(error="Niepoprawny format uuid marketu")

    def test_get_images_when_doesnt_know_market(self, auth_client):
        client, ngo = auth_client
        response = client.get('/api/images/?market_id={}'.format(uuid4()))
        assert response.status_code == 404
        assert response.json() == dict(error="Zapytanie prosi o obrazki do nieznanego marketu")

    def test_get_images_when_market_doesnt_have_any(self, auth_client):
        client, ngo = auth_client
        market = Market.objects.create(owner=ngo, title="1", hashtag="#1")
        response = client.get('/api/images/?market_id={}'.format(market.id))
        assert response.status_code == 200
        assert response.json() == []
