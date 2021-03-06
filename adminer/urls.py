from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "adminer"
urlpatterns = [
    path('polls/create_pdf/<int:id>/', views.create_pdf, name='create_pdf'),
    path('polls/stat_ajax/<int:id>/', views.stat_ajax, name='stat_ajax'),
    path('polls/statistic/<int:id>/', views.polls_stat, name='polls_stat'),
    path('polls/start/<int:id>/', views.polls_start, name='polls_start'),
    path('polls/end/<int:id>/', views.polls_end, name='polls_end'),
    path('polls/show/<int:id>/', views.polls_show, name='polls_show'),
    path('polls/copy/<int:id>/', views.polls_copy, name='polls_copy'),
    path('polls/delete/<int:id>/', views.polls_delete, name='polls_delete'),
    path('polls/edit/<int:id>/', views.polls_edit, name='polls_edit'),
    path('polls/create/', views.polls_create, name='polls_create'),
    path('polls/', views.polls, name='polls'),

    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/', views.category, name='category'),

    path('pattern/delete/<int:id>/', views.pattern_delete, name='pattern_delete'),
    path('pattern/edit/<int:id>/', views.pattern_edit, name='pattern_edit'),
    path('pattern/create/', views.pattern_create, name='pattern_create'),
    path('pattern/get/<int:id>/', views.pattern_get, name='pattern_get'),
    path('pattern/', views.pattern, name='pattern'),

    path('exit/', views.exit, name='exit'),
    path('', views.home, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
