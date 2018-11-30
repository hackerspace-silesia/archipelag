from uuid import uuid4
import os

from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import ImageField
from django.db.models import UUIDField
from django.db.models import CASCADE
from django.utils.safestring import mark_safe
from django.conf import settings

from archipelag.ngo.models import NgoUser


class Market(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    owner = ForeignKey(NgoUser, on_delete=CASCADE)
    title = CharField(max_length=120, blank=True, null=False)
    date_starting = DateTimeField(null=True, blank=True)
    date_ending = DateTimeField(null=True, blank=True)
    date_created = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    hashtag = CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return str(self.title)


class Image(Model):
    market = ForeignKey(Market, null=False, on_delete=CASCADE)
    image_path = ImageField(upload_to="media/", null=True, blank=True)

    def url(self):
        return os.path.join('/', settings.MEDIA_URL, 'media', os.path.basename(str(self.image_path)))

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()))
    image_tag.short_description = 'image_path'

    def __str__(self):
        return str(self.image_path)
