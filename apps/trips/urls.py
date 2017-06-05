from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^trip$', views.trip, name='trip'),
    url(r'^add_trip$', views.add_trip, name='add_trip'),
    url(r'^join/(?P<id>\d+)$', views.join, name='join'),
]
