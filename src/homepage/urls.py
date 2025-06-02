from django.urls import path
from homepage import views


urlpatterns = [
    path('', views.index, name='index'),
    path('guide_body/', views.guide_body, name='guide_body'),
    path('index_body/', views.index_body, name='index_body'),
    path('test_page/', views.test_page, name='test_page'),
    path('translate/', views.translate, name='translate'),
    path("download/", views.download_file, name="download_file"),

]