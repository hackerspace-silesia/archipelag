from django.contrib.admin import ModelAdmin
from django.contrib.admin import site
from django.utils.html import format_html
from django.conf import settings

from archipelag.market.models import Market
from archipelag.market.models import Image


class MarketAdmin(ModelAdmin):
    pass


class ImageAdmin(ModelAdmin):
    pass

site.register(Market, MarketAdmin)
site.register(Image, ImageAdmin)







