from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url('interval-fetching', views.interval_fetching, name='interval-fetching'),
    url('ranking/', views.index, name='index'),
    path('ranker/<str:topic>/', views.ranker),
    url('ranker/all/', views.ranker_all)
]
