"""archipelag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
router.register(r'api/message', MessagesList, base_name='messages_list')
router.register(r'api/messages_types', MessagesTypesList, base_name='messages_types_list')
urlpatterns.extend(router.urls)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

