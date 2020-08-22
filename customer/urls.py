from django.conf.urls import include, url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^save_mem_visit/$', views.save_mem_visit, name='save_mem_visit'),
    url(r'^save_non_mem_visit/$', views.save_non_mem_visit, name='save_non_mem_visit'),
    url(r'^details/$', views.details, name='details'),
    url(r'^membership/$', views.membership, name='membership'),
    url(r'^update_membership/(?P<cust_id>[\w\-]+)/$', views.update_membership, name='update_membership'),
    url(r'^delete_membership/(?P<cust_id>[\w\-]+)/$', views.delete_membership, name='delete_membership'),
    url(r'^delete_client_visit/(?P<visit_id>[\w\-]+)/$', views.delete_client_visit, name='delete_client_visit'),
    url(r'^update_mem_client_visit/(?P<visit_id>[\w\-]+)/$', views.update_mem_client_visit, name='update_mem_client_visit'),
    url(r'^update_non_mem_client_visit/(?P<visit_id>[\w\-]+)/$', views.update_non_mem_client_visit, name='update_non_mem_client_visit'),
]

urlpatterns += staticfiles_urlpatterns()