from django.conf.urls import include, url
from . import views
# from messageManagement.views import daily_check

urlpatterns = [
    url(r'^send/$', views.send, name='send'),
    url(r'^daily_check/$', views.daily_check, name='daily_check'),
    url(r'^addevent/$', views.addevent, name='addevent'),
    url(r'^email/$', views.email, name='email'),
    url(r'^deleteDB/$', views.deleteDB, name='deleteDB'),
    url(r'^exportDB/$', views.exportDB, name='exportDB'),
    url(r'^importDB/$', views.importDB, name='importDB'),
]