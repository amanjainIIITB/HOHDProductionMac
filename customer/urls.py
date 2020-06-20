from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^details/$', views.details, name='details'),
    url(r'^membership/$', views.membership, name='membership'),
    url(r'^update_membership/(?P<cust_id>[\w\-]+)/$', views.update_membership, name='update_membership'),
]