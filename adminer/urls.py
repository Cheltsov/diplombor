from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "adminer"
urlpatterns = [
    path('pattern/delete/<int:id>/', views.pattern_delete, name='pattern_delete'),
    path('pattern/edit/<int:id>/', views.pattern_edit, name='pattern_edit'),
    path('pattern/create/', views.pattern_create, name='pattern_create'),
    path('pattern/', views.pattern, name='pattern'),
    path('exit/', views.exit, name='exit'),
    path('', views.home, name='home'),
]
