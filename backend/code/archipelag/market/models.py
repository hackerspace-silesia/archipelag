from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import ImageField
from django.db.models import URLField

from archipelag.ngo.models import NgoUser


class Market(Model):
    owner = ForeignKey(NgoUser)
    title = CharField(max_length=120, blank=True, null=False)
    url = URLField(null=True)
    date_starting = DateTimeField(null=True, blank=True)
    date_ending = DateTimeField(null=True, blank=True)
    date_created = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    hashtag = CharField(max_length=15, default='')

    def __str__(self):
        return str(self.title)


class Image(Model):
    market = ForeignKey(Market, null=False)
    file = ImageField(upload_to='photos/')
    uploaded = DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file)
