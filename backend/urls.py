"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from .views import  custom_404



from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("album/",include('album.urls')),
    path("genre/",include('genre.urls')),
    path("users/",include("Cusers.urls")),
    path("roles/",include("Roles.urls")),
    path("track/",include("track.urls")),
    path("tour/",include("tour.urls")),
    path("report/",include("report_ban.urls")),
    path('stats/', include('stats.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404

