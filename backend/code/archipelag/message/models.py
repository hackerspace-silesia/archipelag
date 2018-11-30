from django.db import models
from django.db.models import ForeignKey
from django.db.models import TextField
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import PositiveIntegerField
from django.db.models import CASCADE

from archipelag.market.models import Market


class MessageType(models.Model):
    CATEGORIES = (
        ('Facebook', 'Facebook'),
        ('Prasa', 'Informacja Prasowa'),
        ('Newsletter', 'Newsletter'),
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('SMS', 'SMS Kiss'),
    )
    service = CharField(max_length=10, choices=CATEGORIES, default='Facebook')
    count_hashtag = BooleanField(default=True, blank=True)
    char_restriction = PositiveIntegerField(null=False, blank=True)

    def __str__(self):
        return self.service


class Message(models.Model):
    content = TextField(max_length=2048, blank=True)
    shared = PositiveIntegerField(default=0)
    type = ForeignKey(MessageType, null=False, on_delete=CASCADE)
    market = ForeignKey(Market, null=False, on_delete=CASCADE)

    def __str__(self):
        return str(self.content)[0:25]
