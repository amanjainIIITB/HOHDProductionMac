from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup_view, name='signup_view'),
    url(r'^$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^change_password/$', views.change_password, name='change_password')
]