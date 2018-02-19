from archipelag.market.models import Market
from archipelag.market.models import Image
from django.contrib.admin import ModelAdmin
from django.contrib.admin import site


class MarketAdmin(ModelAdmin):
    pass

site.register(Market, MarketAdmin)
site.register(Image, MarketAdmin)
