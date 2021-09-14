from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include("adminer.urls")),
    path('user/', include("user.urls")),
    path('', include("auth.urls")),
]