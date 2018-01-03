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

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/market/', permanent=False), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^market/', include('archipelag.market.urls')),
    url(r'^message/', include('archipelag.message.urls'), ),
    url(r'^event_log/', include('archipelag.event_log.urls'), ),
    url(r'^share_log/', include('archipelag.share_log.urls'), ),
]

if not settings.DEBUG:
    # TODO: implement nginx support in docker-compose
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

