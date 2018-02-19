from django.contrib.admin import ModelAdmin
from django.contrib.admin import site
from django.utils.html import format_html

from archipelag.market.models import Market
from archipelag.market.models import Image


class MarketAdmin(ModelAdmin):
    pass

def image_tag(url):
    return format_html(
        "<img src='code/archipelag/market/images/{url}' />".format(
            url=url,
        )
    )


class ImageAdmin(ModelAdmin):
    list_display = (
        'image_path', 'market'
    )
    list_display_links = ('image_path', 'market')
    fields = ('market', 'image_path')

    def show_image(self, obj):
        image = obj.image_path
        return image_tag(image)

site.register(Market, MarketAdmin)
site.register(Image, ImageAdmin)







