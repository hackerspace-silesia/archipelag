from archipelag.ngo.models import NgoUser
from django.contrib.auth.models import User
from pytest import mark
from pytest import fixture
from rest_framework.test import APIClient


@mark.django_db
class BaseTestCase(object):

    @fixture
    def user_with_ngo(self):
        email = 'jpueblo@example.com'
        username = 'jpueblo'
        password = 'password'
        user = User.objects.create_user(
            username, email, password)
        ngo = NgoUser.objects.create(
            user=user, organisation="org", coins=10)
        return user, ngo

    @fixture
    def auth_client(self, user_with_ngo):
        user, ngo = user_with_ngo
        client = APIClient()
        client.force_authenticate(user)
        return client, ngo
