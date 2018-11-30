from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from archipelag.message.views import MessagesList
from archipelag.message.views import MessagesTypesList
from archipelag.ngo.views import NgoUserList
from archipelag.market.views import UploadedImagesViewSet

from rest_framework.routers import DefaultRouter


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api/market/', permanent=False), name='index'),
    url(r'^api/admin/', admin.site.urls),
    url(r'^api/accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^api/accounts/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/market/', include('archipelag.market.urls')),
    url(r'^api/event_log/', include('archipelag.event_log.urls'), ),
    url(r'^api/share_log/', include('archipelag.share_log.urls'), ),
    url(r'^api/ngo/', include('archipelag.ngo.urls'), ),
]


router = DefaultRouter()
router.register(r'api/message', MessagesList, basename='messages_list')
router.register(r'api/messages_types', MessagesTypesList, basename='messages_types_list')
router.register(r'api/ngo', NgoUserList, basename='all_ngos')
router.register(r'api/images', UploadedImagesViewSet, basename='images')
urlpatterns.extend(router.urls)
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
# if not settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

