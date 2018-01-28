from django.db.models import BooleanField
from django.db.models import CASCADE
from django.db.models import ForeignKey
from django.db.models import Model

from archipelag.market.models import Market
from archipelag.ngo.models import NgoUser


class Notification(Model):
    owner = ForeignKey(NgoUser, on_delete=CASCADE)
    event = ForeignKey(Market, on_delete=CASCADE)
    sent = BooleanField(default=False, null=False)