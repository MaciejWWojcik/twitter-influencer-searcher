from django.conf.urls import url

from . import views

urlpatterns = [
    url('interval-fetching', views.interval_fetching, name='interval-fetching'),
    url('', views.index, name='index'),
]
