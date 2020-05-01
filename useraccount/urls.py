from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup_view, name='signup_view'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
]