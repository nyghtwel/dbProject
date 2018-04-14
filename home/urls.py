from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('query1', views.query1, name='query1'),
    path('data_set', views.data_set, name='data_set'),
    path('query2', views.index, name='query2'),
]
