from django.conf.urls import url

from archipelag.share_log.views import ShareLogList

urlpatterns = [
    url(r'^(?P<market_id>.+)/$', ShareLogList.as_view()),
]
