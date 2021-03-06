from django.conf.urls import include, url
from . import views, analysis, expense_report
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # APIs
    url(r'^getAnalysis/$', analysis.AnalysisReport.as_view()),
    url(r'^getExpense/$', expense_report.ExpenseReport.as_view()),

    # Non-APIs
    # Analytics
    url(r'^analysis/$', views.analysis, name='analysis'),

    # Employees
    url(r'^employee/$', views.employee, name='employee'),
    url(r'^create_employee/$', views.create_employee, name='create_employee'),
    url(r'^update_employee/(?P<employee_id>[\w\-]+)/$', views.update_employee, name='update_employee'),
    url(r'^delete_employee/(?P<employee_id>[\w\-]+)/$', views.delete_employee, name='delete_employee'),
    url(r'^download_appointment_letter/(?P<employee_id>[\w\-]+)/$', views.download_appointment_letter, name='download_appointment_letter'),
    url(r'^download_employee_govt_id/(?P<employee_id>[\w\-]+)/$', views.download_employee_govt_id, name='download_employee_govt_id'),

    # Expense
    url(r'^expense/$', views.expense, name='expense'),
    url(r'^update_expense/(?P<expense_id>[\w\-]+)/$', views.update_expense, name='update_expense'),
    url(r'^delete_expense/(?P<expense_id>[\w\-]+)/$', views.delete_expense, name='delete_expense'),
    url(r'^add_expense/$', views.add_expense, name='add_expense'),

    # Appointment
    url(r'^appointment/$', views.appointment, name='appointment'),
    url(r'^save_mem_client_appointment/$', views.save_mem_client_appointment, name='save_mem_client_appointment'),
    url(r'^save_non_mem_client_appointment/$', views.save_non_mem_client_appointment, name='save_non_mem_client_appointment'),

    # Parlour/Shop
    url(r'^shopreg/$', views.shopreg, name='shopreg'),
    url(r'^select_parlour/(?P<shop_id>[\w\-]+)/$', views.select_parlour, name='select_parlour'),
    url(r'^edit_parlour/(?P<shop_id>[\w\-]+)/$', views.edit_parlour, name='edit_parlour'),

    # Downloads
    url(r'^download_analysis_report/(?P<month>[\w\-]+)/(?P<year>[\w\-]+)/$', views.download_analysis_report, name='download_analysis_report'),
    url(r'^download_expense_data/(?P<month>[\w\-]+)/(?P<year>[\w\-]+)/$', views.download_expense_data, name='download_expense_data'),
    url(r'^download_customer_data/(?P<month>[\w\-]+)/(?P<year>[\w\-]+)/$', views.download_customer_data, name='download_customer_data'),

    # Add Partner
    url(r'^add_partner/$', views.add_partner, name='add_partner'),

    # Misc
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),

]

urlpatterns += staticfiles_urlpatterns()