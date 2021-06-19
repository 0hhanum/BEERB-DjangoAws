"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# settings.py 를 직접 import 하는 게 아니라 장고 시스템에서 conf 에 clone 된 settings 를 import.


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("users/", include("users.urls", namespace="users")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:  # DEBUG 가 켜져있을 때 (developing 일 때)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# MEDIA_URL 로 접근했을 때 어느 경로를 참조할 것인지
