from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path('create/<int:id>/', views.create_user_answer, name='create_user_answer'),
    path('polls/<int:id>/', views.index, name='index'),
]