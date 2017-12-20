from django.conf.urls import url

from archipelag.market.views import MarketView
from archipelag.market.views import market_create
from archipelag.market.views import get_messages

urlpatterns = [
    url(r'^$', MarketView.as_view(), name="market"),
    url(r'^create/', market_create, name="market_create"),
    url(r'^details/(?P<market_id>\d+)/$', get_messages, name='market_details'),
]