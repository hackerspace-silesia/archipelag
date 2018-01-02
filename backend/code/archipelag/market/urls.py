from django.conf.urls import url

from archipelag.market.views import MarketList
from archipelag.market.views import market_create
from archipelag.market.views import get_messages
from rest_framework.routers import DefaultRouter
router = DefaultRouter()


router.register(r'', MarketList, base_name='market')
#
# urlpatterns = [
#     url(r'^$', MarketList, name="market"),
#     url(r'^create/', market_create, name="market_create"),
#     url(r'^details/(?P<market_id>\d+)/$', get_messages, name='market_details'),
# ]

urlpatterns = router.urls
