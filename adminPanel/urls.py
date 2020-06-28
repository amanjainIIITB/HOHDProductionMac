from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^send/$', views.send, name='send')
]