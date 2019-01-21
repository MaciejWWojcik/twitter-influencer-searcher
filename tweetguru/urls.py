from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url('interval-fetching', views.interval_fetching, name='interval-fetching'),
    # url('', views.index, name='index'),
    path('ranker/<int:topicId>/', views.ranker)
]
