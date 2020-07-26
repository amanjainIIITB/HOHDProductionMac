from django.conf.urls import include, url
from . import views
# from messageManagement.views import daily_check

urlpatterns = [
    url(r'^send/$', views.send, name='send'),
    # url(r'^daily_check/$', messageManagement.views.daily_check, name='daily_check'),
    url(r'^email/$', views.email, name='email'),
    url(r'^exportDB/$', views.exportDB, name='exportDB'),
]