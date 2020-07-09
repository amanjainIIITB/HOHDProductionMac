from django.http import HttpResponse
from customer.models import Membership, BharatPe, Paytm, client
from staff.models import Expense, ShopRegistration, Employee
from useraccount.models import OwnerRegistration
import xlwt
from datetime import datetime, timedelta

def set_table_header(wb, sheet_name, table_header, font_style):
    # adding sheet
    ws = wb.add_sheet(sheet_name)

    # write column headers in sheet
    for col_num in range(len(table_header)):
        ws.write(0, col_num, table_header[col_num], font_style)
    return ws


def get_bharatpe_data(wb, row_num, font_style):
    ws = set_table_header(wb, "bharatpe_data", ['date', 'ShopID', 'bardate', 'time', 'numberofclient', 'amount'], font_style)
    bharatpes = BharatPe.objects.values('date', 'ShopID', 'bardate', 'time', 'numberofclient', 'amount')
    
    for bharatpe in bharatpes:
        row_num = row_num + 1
        ws.write(row_num, 0, bharatpe['date'], font_style)
        ws.write(row_num, 1, bharatpe['ShopID'], font_style)
        ws.write(row_num, 2, bharatpe['bardate'], font_style)
        ws.write(row_num, 3, bharatpe['time'], font_style)
        ws.write(row_num, 4, bharatpe['numberofclient'], font_style)
        ws.write(row_num, 5, bharatpe['amount'], font_style)


def get_paytm_data(wb, row_num, font_style):
    ws = set_table_header(wb, "paytm_data", ['date', 'ShopID', 'bardate', 'time', 'numberofclient', 'amount'], font_style)
    paytms = Paytm.objects.values('date', 'ShopID', 'bardate', 'time', 'numberofclient', 'amount')
    
    for paytm in paytms:
        row_num = row_num + 1
        ws.write(row_num, 0, paytm['date'], font_style)
        ws.write(row_num, 1, paytm['ShopID'], font_style)
        ws.write(row_num, 2, paytm['bardate'], font_style)
        ws.write(row_num, 3, paytm['time'], font_style)
        ws.write(row_num, 4, paytm['numberofclient'], font_style)
        ws.write(row_num, 5, paytm['amount'], font_style)


def get_cash_data(wb, row_num, font_style):
    ws = set_table_header(wb, "cash_data", ['date', 'ShopID', 'bardate', 'time', 'numberofclient', 'amount'], font_style)
    cashs = client.objects.values('date', 'ShopID', 'bardate', 'time', 'numberofclient', 'amount')
    
    for cash in cashs:
        row_num = row_num + 1
        ws.write(row_num, 0, cash['date'], font_style)
        ws.write(row_num, 1, cash['ShopID'], font_style)
        ws.write(row_num, 2, cash['bardate'], font_style)
        ws.write(row_num, 3, cash['time'], font_style)
        ws.write(row_num, 4, cash['numberofclient'], font_style)
        ws.write(row_num, 5, cash['amount'], font_style)


def get_membership_data(wb, row_num, font_style):
    ws = set_table_header(wb, "membership_data", ['custID', 'shopID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit', 'total_amount', 'number_of_visit'], font_style)
    memberships = Membership.objects.values('custID', 'shopID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit', 'total_amount', 'number_of_visit')
    
    for memebership in memberships:
        row_num = row_num + 1
        ws.write(row_num, 0, memebership['custID'], font_style)
        ws.write(row_num, 1, memebership['shopID'], font_style)
        ws.write(row_num, 2, memebership['Contact_Number'], font_style)
        ws.write(row_num, 3, memebership['Sex'], font_style)
        ws.write(row_num, 4, memebership['Name'], font_style)
        ws.write(row_num, 5, memebership['DOB'], font_style)
        ws.write(row_num, 6, memebership['last_visit'], font_style)
        ws.write(row_num, 7, memebership['total_amount'], font_style)
        ws.write(row_num, 8, memebership['number_of_visit'], font_style)


def get_expense_data(wb, row_num, font_style):
    ws = set_table_header(wb, "expense_data", ['ExpenseID', 'date', 'shopID', 'purpose', 'paymentmode', 'comment', 'amount'], font_style)
    expenses = Expense.objects.values('ExpenseID', 'date', 'shopID', 'purpose', 'paymentmode', 'comment', 'amount')
    
    for expense in expenses:
        row_num = row_num + 1
        ws.write(row_num, 0, expense['ExpenseID'], font_style)
        ws.write(row_num, 1, expense['date'], font_style)
        ws.write(row_num, 2, expense['shopID'], font_style)
        ws.write(row_num, 3, expense['purpose'], font_style)
        ws.write(row_num, 4, expense['paymentmode'], font_style)
        ws.write(row_num, 5, expense['comment'], font_style)
        ws.write(row_num, 6, expense['amount'], font_style)


def get_shop_registration_data(wb, row_num, font_style):
    ws = set_table_header(wb, "shop_registration_data", ['ShopID', 'Desk_Contact_Number', 'Shop_Name', 'Shop_Address', 'owner_list'], font_style)
    shop_registrations = ShopRegistration.objects.values('ShopID', 'Desk_Contact_Number', 'Shop_Name', 'Shop_Address', 'owner_list')
    
    for shop_registration in shop_registrations:
        row_num = row_num + 1
        ws.write(row_num, 0, shop_registration['ShopID'], font_style)
        ws.write(row_num, 1, shop_registration['Desk_Contact_Number'], font_style)
        ws.write(row_num, 2, shop_registration['Shop_Name'], font_style)
        ws.write(row_num, 3, shop_registration['Shop_Address'], font_style)
        ws.write(row_num, 4, shop_registration['owner_list'], font_style)


def get_employee_data(wb, row_num, font_style):
    ws = set_table_header(wb, "employee_data", ['EmployeeID', 'ShopID', 'name', 'contact_number', 'age', 'sex', 'date_of_joining', 'DOB', 'temporary_address', 'permanent_address'], font_style)
    employees = Employee.objects.values('EmployeeID', 'ShopID', 'name', 'contact_number', 'age', 'sex', 'date_of_joining', 'DOB', 'temporary_address', 'permanent_address')
    
    for employee in employees:
        row_num = row_num + 1
        ws.write(row_num, 0, employee['EmployeeID'], font_style)
        ws.write(row_num, 1, employee['ShopID'], font_style)
        ws.write(row_num, 2, employee['name'], font_style)
        ws.write(row_num, 3, employee['contact_number'], font_style)
        ws.write(row_num, 4, employee['age'], font_style)
        ws.write(row_num, 5, employee['sex'], font_style)
        ws.write(row_num, 6, employee['date_of_joining'], font_style)
        ws.write(row_num, 7, employee['DOB'], font_style)
        ws.write(row_num, 8, employee['temporary_address'], font_style)
        ws.write(row_num, 9, employee['permanent_address'], font_style)


def get_owner_registration_data(wb, row_num, font_style):
    ws = set_table_header(wb, "owner_registration_data", ['user', 'Contact_Number', 'username', 'ownerID', 'Name', 'shop_list'], font_style)
    owner_registrations = OwnerRegistration.objects.values('user', 'Contact_Number', 'username', 'ownerID', 'Name', 'shop_list')
    
    for owner_registration in owner_registrations:
        row_num = row_num + 1
        ws.write(row_num, 0, owner_registration['user'], font_style)
        ws.write(row_num, 1, owner_registration['Contact_Number'], font_style)
        ws.write(row_num, 2, owner_registration['username'], font_style)
        ws.write(row_num, 3, owner_registration['ownerID'], font_style)
        ws.write(row_num, 4, owner_registration['Name'], font_style)
        ws.write(row_num, 5, owner_registration['shop_list'], font_style)


def get_complete_database():
    print('Excel file is getting ready')

    # current date and time
    now = datetime.now() + timedelta(hours=5, minutes=30)

    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename='+str(now.strftime("%d/%m/%Y %H:%M:%S"))+'-DB.xls'
    
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    get_bharatpe_data(wb, row_num, font_style)
    get_paytm_data(wb, row_num, font_style)
    get_cash_data(wb, row_num, font_style)
    get_membership_data(wb, row_num, font_style)
    get_expense_data(wb, row_num, font_style)
    get_shop_registration_data(wb, row_num, font_style)
    get_employee_data(wb, row_num, font_style)
    get_owner_registration_data(wb, row_num, font_style)
    wb.save(response)
    return response