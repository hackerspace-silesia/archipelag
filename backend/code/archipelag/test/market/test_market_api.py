from unittest.mock import patch

from rest_framework.test import APIClient
from django.forms.models import model_to_dict

from archipelag.market.models import Market
from archipelag.test.base_test_case import BaseTestCase


class TestMarketApi(BaseTestCase):

    def test_create_market_when_not_jwt(self):
        client = APIClient().post('/api/market/', format='json')
        assert client.json()[
            "detail"] == 'Authentication credentials were not provided.'

    @patch('archipelag.market.views.MarketList.permission_classes', [])
    def test_get_market_ordered_by_newest(self, user_with_ngo):
        # given
        user, ngo = user_with_ngo
        expected_market = Market.objects.create(
            owner=ngo, title="1", hashtag="#1")
        expected_market2 = Market.objects.create(
            owner=ngo, title="2", hashtag="#2")
        # when
        market_list = APIClient().get('/api/market/', format="json").json()
        # then
        oldest_market = model_to_dict(expected_market)
        newest_market = model_to_dict(expected_market2)
        assert market_list[0]["title"] == newest_market['title']
        assert market_list[1]["title"] == oldest_market['title']

    def test_correct_create_market(self, auth_client):
        market = {
            'body': {
                'title': 'jjj',
                'hashtag': 'hh',
                'date_starting': '2018-02-20 23:50',
                'date_ending': '2018-02-20 23:50'
            }
        }
        client, ngo = auth_client
        response = client.post('/api/market/', market, format="json")

        assert "success" in response.json()
        assert response.status_code == 200

    def test_create_market_when_user_hasnt_coins(self, auth_client):
        client, ngo = auth_client
        ngo.coins = 2.9
        ngo.save()
        market = {'body': {'title': 'jjj'}}
        response = client.post('/api/market/', market, format="json")

        assert response.json() == {"error": "Za mało punktów."}
        assert response.status_code == 200

    def test_create_market_when_missing_required_field(self, auth_client):
        client, ngo = auth_client
        market = {'body': {}}
        response = client.post('/api/market/', market, format="json")

        assert response.json() == {
            "error": {
                'title': ['This field is required.']
            }
        }
        assert response.status_code == 400

    def test_create_market_when_wrong_date(self, auth_client):
        client, ngo = auth_client
        market = {'body': {'title': 'jjj', 'date_starting': 'yyu'}}
        response = client.post('/api/market/', market, format="json")

        assert response.json() == {
            "error": {
                'date_starting': [
                    'Datetime has wrong format. Use one of these formats '
                    'instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
                ]
            }
        }
        assert response.status_code == 400

    def test_create_market_when_not_know_field(self, auth_client):
        client, ngo = auth_client
        market = {
            'body': {
                'title': 'jjj',
                'hashtag': 'hh',
                'h': '2018-02-20 23:50'
            }
        }
        response = client.post('/api/market/', market, format="json")

        assert response.json() == {
            "error": "'h' is an invalid keyword argument for this function"
        }
        assert response.status_code == 400
