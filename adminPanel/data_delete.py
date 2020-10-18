from django.http import HttpResponse
from customer.models import Membership, ClientVisit, AllService, Services
from staff.models import Expense, ShopRegistration, Employee
from useraccount.models import OwnerRegistration


def delete_client_visit_data():
    print('Deleting cash visit records')
    ClientVisit.objects.all().delete()


def delete_membership_data():
    print('Deleting membership records')
    Membership.objects.all().delete()


def delete_expense_data():
    print('Deleting expense records')
    Expense.objects.all().delete()
    

def delete_shop_registration_data():
    print('Deleting Shop Registration records')
    ShopRegistration.objects.all().delete()


def delete_employee_data():
    print('Deleting Employee records')
    Employee.objects.all().delete()


def delete_owner_registration_data():
    print('Deleting Owner Registration records')
    OwnerRegistration.objects.all().delete()


def delete_services_data():
    print('Deleting Service name records')
    Services.objects.all().delete()


def delete_all_services_data():
    print('Deleting Client Service records')
    AllService.objects.all().delete()


def delete_complete_database():
    print('Deleting DB entries')

    delete_client_visit_data()
    delete_membership_data()
    delete_expense_data()
    delete_shop_registration_data()
    delete_employee_data()
    delete_owner_registration_data()
    delete_services_data()
    delete_all_services_data()

    print('All DB entries deleted Successfully')