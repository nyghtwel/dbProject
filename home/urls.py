from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('national_avg', views.national_avg, name='national_avg'),
    path('top_10', views.top_10, name='top_10'),
    path('time', views.time, name='time'),
    path('indicators', views.indicators, name='indicators'),
    path('location', views.location, name='location'),
    path('users', views.user, name='user'),
    path('export_csv_file/<data>/', views.export_csv_file, name='export_csv_file')
]
