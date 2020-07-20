from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^send/$', views.send, name='send'),
    url(r'^email/$', views.email, name='email'),
    url(r'^exportDB/$', views.exportDB, name='exportDB'),
]