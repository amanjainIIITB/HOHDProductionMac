from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^(?P<shop_id>[\w\-]+)/$', views.room, name='room')
]
