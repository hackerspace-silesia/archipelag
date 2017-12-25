from django.conf.urls import url

from archipelag.event_log.views import EventLogList

urlpatterns = [
    url(r'^(?P<type>.+)/(?P<id_connected_object>.+)/$', EventLogList.as_view()),
]
