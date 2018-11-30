from archipelag.market.views import MarketList, UploadedImagesViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'', MarketList, basename='market')
urlpatterns = router.urls
