from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^details/$', views.details, name='details'),
    url(r'^membership/$', views.membership, name='membership'),
]