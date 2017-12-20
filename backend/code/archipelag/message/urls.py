from django.conf.urls import url
from archipelag.message.views import message_create
from archipelag.message.views import add_coins_for_share

urlpatterns = [
    url(r'^create/(?P<market_id>\d+)/$', message_create, name="message_create"),
    url(r'^add_point/(?P<message_id>\d+)/$', add_coins_for_share, name='add_coins_for_share'),
]
