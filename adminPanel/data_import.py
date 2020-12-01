from django.http import HttpResponse
from customer.models import Membership, ClientVisit, AllService, Services
from staff.models import Expense, ShopRegistration, Employee, Appointment
from useraccount.models import OwnerRegistration
import xlwt
import xlrd
import pandas
from HOHDProductionMac.common_function import get_current_date
from .data_delete import delete_complete_database
from datetime import datetime


def put_client_visit_data(file):
    df = pandas.read_excel(file, sheet_name='client_visit_data')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        ClientVisit(visitID=row["visitID"], isMember=row["isMember"], custID=row["custID"], date=str(row["date"]).split(" ")[0], employee_id=row["employee_id"], payment_mode=row["payment_mode"], ShopID=row["ShopID"], time=row["time"], numberofclient=row["numberofclient"], amount=row["amount"], services=row["services"]).save()


def put_membership_data(file):
    df = pandas.read_excel(file, sheet_name='membership_data')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        Membership(custID=row["custID"], shopID=row["shopID"], Contact_Number=row["Contact_Number"], Sex=row["Sex"], Name=row["Name"], DOB=str(row["DOB"]).split(" ")[0], last_visit=str(row["last_visit"]).split(" ")[0]).save()


def put_expense_data(file):
    df = pandas.read_excel(file, sheet_name='expense_data')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        Expense(ExpenseID=row["ExpenseID"], date=str(row["date"]).split(" ")[0], shopID=row["shopID"], purpose=row["purpose"], paymentmode=row["paymentmode"], comment=row["comment"], amount=row["amount"]).save()
    

def put_shop_registration_data(file):
    df = pandas.read_excel(file, sheet_name='shop_registration_data')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        ShopRegistration(ShopID=row["ShopID"], Desk_Contact_Number=row["Desk_Contact_Number"], Shop_Name=row["Shop_Name"], Shop_Address=row["Shop_Address"]).save()


def put_employee_data(file):
    df = pandas.read_excel(file, sheet_name='employee_data')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        Employee(EmployeeID=row["EmployeeID"], ShopID=row["ShopID"], name=row["name"], contact_number=row["contact_number"], sex=row["sex"], date_of_joining=str(row["date_of_joining"]).split(" ")[0], DOB=str(row["DOB"]).split(" ")[0], temporary_address=row["temporary_address"], permanent_address=row["permanent_address"]).save()


def put_appointment_data(file):
    df = pandas.read_excel(file, sheet_name='appointment_data')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        Appointment(name=row["name"], contact_number=row["contact_number"], date=str(row["date"]).split(" ")[0], start_time=row["start_time"], end_time=row["end_time"]).save()


def put_owner_registration_data(file):
    df = pandas.read_excel(file, sheet_name='owner_registration_data')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        OwnerRegistration(phone=row["phone"], ownerID=row["ownerID"], Name=row["Name"], shop_list=row["shop_list"]).save()


def put_services_data(file):
    df = pandas.read_excel(file, sheet_name='Services_data')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        Services(visitID=row["visitID"], date=str(row["date"]).split(" ")[0], time=row["time"], shopID=row["shopID"], ServiceID=row["ServiceID"]).save()


def put_all_services_data(file):
    df = pandas.read_excel(file, sheet_name='All_Services')
    df = df.fillna("")
    for index, row in df.iterrows(): 
        AllService(ServiceID=row["ServiceID"], Name=row["Name"]).save()


def put_complete_database(file):
    print('Excel file is getting uploaded')

    # set date format
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy-mm-dd'

    # Delete old data
    delete_complete_database()

    #Enter Fresh Data
    put_client_visit_data(file)
    put_membership_data(file)
    put_expense_data(file)
    put_shop_registration_data(file)
    put_employee_data(file)
    put_appointment_data(file)
    put_owner_registration_data(file)
    put_services_data(file)
    put_all_services_data(file)