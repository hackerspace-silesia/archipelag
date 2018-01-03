from django.conf.urls import url

from archipelag.share_log.views import ShareLogList

urlpatterns = [
    url(r'^(?P<shared_message>.+)/$', ShareLogList.as_view()),
]
