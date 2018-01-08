from django.conf.urls import url

from archipelag.share_log.views import ShareLogList

urlpatterns = [
    url(r'^(?P<market_id>.+)/$', ShareLogList.as_view({'get': 'get_list', 'post': 'create'})),
]

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
#
#
# router.register(r'', ShareLogList, base_name='share_log')
# urlpatterns = router.urls