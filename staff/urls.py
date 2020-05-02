from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^analysis/$', views.analysis, name='analysis'),
    url(r'^getAnalysis/$', views.AnalysisReport.as_view()),
    url(r'^getExpense/$', views.ExpenseReport.as_view()),
    url(r'^download/(?P<download_type>[\w\-]+)/(?P<month>[\w\-]+)/(?P<year>[\w\-]+)/$', views.download, name='download'),
    url(r'^expense/$', views.expense, name='expense'),
    url(r'^storeExpense/$', views.storeExpense, name='storeExpense'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^shopreg/$', views.shopreg, name='shopreg'),
]