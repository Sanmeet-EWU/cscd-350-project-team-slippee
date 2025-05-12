from django.urls import path
from src.homepage import views


urlpatterns = [
    path('', views.index, name='index'),
]