from archipelag.message.views import MessagesList
from django.conf.urls import url
# urlpatterns = [
# # #     # url(r'^create/(?P<market_id>\d+)/$', message_create, name="message_create"),
# # #     # url(r'^add_point/(?P<message_id>\d+)/$', add_coins_for_share, name='add_coins_for_share'),
# #     url('^detail/(?P<market_id>\d+)/$', MessagesList.as_view()),
# ]



from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'', MessagesList, base_name='messages_list')
urlpatterns = router.urls