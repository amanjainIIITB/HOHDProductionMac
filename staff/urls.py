from django.conf.urls import include, url
from . import views, analysis, expense_report

urlpatterns = [
    # API
    url(r'^getAnalysis/$', analysis.AnalysisReport.as_view()),
    url(r'^getExpense/$', expense_report.ExpenseReport.as_view()),

    # Non-API
    url(r'^analysis/$', views.analysis, name='analysis'),
    url(r'^download/(?P<download_type>[\w\-]+)/(?P<month>[\w\-]+)/(?P<year>[\w\-]+)/$', views.download, name='download'),
    url(r'^expense/$', views.expense, name='expense'),
    url(r'^update_expense/(?P<expense_id>[\w\-]+)/$', views.update_expense, name='update_expense'),
    url(r'^delete_expense/(?P<expense_id>[\w\-]+)/$', views.delete_expense, name='delete_expense'),
    url(r'^employee/$', views.employee, name='employee'),
    url(r'^update_employee/(?P<employee_id>[\w\-]+)/$', views.update_employee, name='update_employee'),
    url(r'^delete_employee/(?P<employee_id>[\w\-]+)/$', views.delete_employee, name='delete_employee'),
    url(r'^add_expense/$', views.add_expense, name='add_expense'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^shopreg/$', views.shopreg, name='shopreg'),
    url(r'^add_partner/$', views.add_partner, name='add_partner'),
    url(r'^select_parlour/(?P<shop_id>[\w\-]+)/$', views.select_parlour, name='select_parlour'),
]