from archipelag.ngo.models import NgoUser
from django.contrib.auth.models import User
from django.test import TransactionTestCase


class BaseTestCase(TransactionTestCase):

    def setUp(self):
        email = 'jpueblo@example.com'
        username = 'jpueblo'
        password = 'password'
        self.user = User.objects.create_user(
            username, email, password)
        self.ngo = NgoUser.objects.create(
            user=self.user, organisation="org", coins=10)
