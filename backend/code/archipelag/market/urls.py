from archipelag.market.views import MarketList
from rest_framework.routers import DefaultRouter
router = DefaultRouter()


router.register(r'', MarketList, base_name='market')
urlpatterns = router.urls
