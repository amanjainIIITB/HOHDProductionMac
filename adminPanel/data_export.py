from django.http import HttpResponse
from customer.models import Membership, ClientVisit, AllService, Services
from staff.models import Expense, ShopRegistration, Employee, Appointment
from useraccount.models import OwnerRegistration
import xlwt

from HOHDProductionMac.common_function import get_current_date


def set_table_header(wb, sheet_name, table_header, font_style):
    # adding sheet
    ws = wb.add_sheet(sheet_name)

    # write column headers in sheet
    for col_num in range(len(table_header)):
        ws.write(0, col_num, table_header[col_num], font_style)
    return ws


def get_client_visit_data(wb, row_num, date_format, time_format, font_style):
    column_names = ['visitID', 'isMember', 'custID', 'date', 'employee_id', 'payment_mode', 'ShopID', 'time', 'numberofclient', 'amount', 'services']
    ws = set_table_header(wb, "client_visit_data", column_names, font_style)
    clientvisits = ClientVisit.objects.values('visitID', 'isMember', 'custID', 'date', 'employee_id', 'payment_mode', 'ShopID', 'time', 'numberofclient', 'amount', 'services')
    
    for clientvisit in clientvisits:
        row_num = row_num + 1
        ws.write(row_num, 0, clientvisit['visitID'], font_style)
        ws.write(row_num, 1, clientvisit['isMember'], font_style)
        ws.write(row_num, 2, clientvisit['custID'], font_style)
        ws.write(row_num, 3, clientvisit['date'], date_format)
        ws.write(row_num, 4, clientvisit['employee_id'], font_style)
        ws.write(row_num, 5, clientvisit['payment_mode'], font_style)
        ws.write(row_num, 6, clientvisit['ShopID'], font_style)
        ws.write(row_num, 7, clientvisit['time'], time_format)
        ws.write(row_num, 8, clientvisit['numberofclient'], font_style)
        ws.write(row_num, 9, clientvisit['amount'], font_style)
        ws.write(row_num, 10, clientvisit['services'], font_style)


def get_membership_data(wb, row_num, date_format, font_style):
    column_names = ['custID', 'shopID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit']
    ws = set_table_header(wb, "membership_data", column_names, font_style)
    memberships = Membership.objects.values('custID', 'shopID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit')
    
    for memebership in memberships:
        row_num = row_num + 1        
        ws.write(row_num, 0, memebership['custID'], font_style)
        ws.write(row_num, 1, memebership['shopID'], font_style)
        ws.write(row_num, 2, memebership['Contact_Number'], font_style)
        ws.write(row_num, 3, memebership['Sex'], font_style)
        ws.write(row_num, 4, memebership['Name'], font_style)
        ws.write(row_num, 5, memebership['DOB'], date_format)
        ws.write(row_num, 6, memebership['last_visit'], date_format)


def get_expense_data(wb, row_num, date_format, font_style):
    column_names = ['ExpenseID', 'date', 'shopID', 'purpose', 'paymentmode', 'comment', 'amount']
    ws = set_table_header(wb, "expense_data", column_names, font_style)
    expenses = Expense.objects.values('ExpenseID', 'date', 'shopID', 'purpose', 'paymentmode', 'comment', 'amount')
    
    for expense in expenses:
        row_num = row_num + 1
        ws.write(row_num, 0, expense['ExpenseID'], font_style)
        ws.write(row_num, 1, expense['date'], date_format)
        ws.write(row_num, 2, expense['shopID'], font_style)
        ws.write(row_num, 3, expense['purpose'], font_style)
        ws.write(row_num, 4, expense['paymentmode'], font_style)
        ws.write(row_num, 5, expense['comment'], font_style)
        ws.write(row_num, 6, expense['amount'], font_style)


def get_shop_registration_data(wb, row_num, font_style):
    column_names = ['ShopID', 'Desk_Contact_Number', 'Shop_Name', 'Shop_Address', 'owner_list']
    ws = set_table_header(wb, "shop_registration_data", column_names, font_style)
    shop_registrations = ShopRegistration.objects.values('ShopID', 'Desk_Contact_Number', 'Shop_Name', 'Shop_Address', 'owner_list')
    
    for shop_registration in shop_registrations:
        row_num = row_num + 1
        ws.write(row_num, 0, shop_registration['ShopID'], font_style)
        ws.write(row_num, 1, shop_registration['Desk_Contact_Number'], font_style)
        ws.write(row_num, 2, shop_registration['Shop_Name'], font_style)
        ws.write(row_num, 3, shop_registration['Shop_Address'], font_style)
        ws.write(row_num, 4, shop_registration['owner_list'], font_style)


def get_employee_data(wb, row_num, date_format, font_style):
    column_names = ['EmployeeID', 'ShopID', 'name', 'contact_number', 'sex', 'date_of_joining', 'DOB', 'temporary_address', 'permanent_address']
    ws = set_table_header(wb, "employee_data", column_names, font_style)
    employees = Employee.objects.values('EmployeeID', 'ShopID', 'name', 'contact_number', 'sex', 'date_of_joining', 'DOB', 'temporary_address', 'permanent_address')
    
    for employee in employees:
        row_num = row_num + 1
        ws.write(row_num, 0, employee['EmployeeID'], font_style)
        ws.write(row_num, 1, employee['ShopID'], font_style)
        ws.write(row_num, 2, employee['name'], font_style)
        ws.write(row_num, 3, employee['contact_number'], font_style)
        ws.write(row_num, 4, employee['sex'], font_style)
        ws.write(row_num, 5, employee['date_of_joining'], date_format)
        ws.write(row_num, 6, employee['DOB'], date_format)
        ws.write(row_num, 7, employee['temporary_address'], font_style)
        ws.write(row_num, 8, employee['permanent_address'], font_style)


def get_owner_registration_data(wb, row_num, font_style):
    column_names = ['phone', 'ownerID', 'Name', 'shop_list']
    ws = set_table_header(wb, "owner_registration_data", column_names, font_style)
    owner_registrations = OwnerRegistration.objects.values('phone', 'ownerID', 'Name', 'shop_list')
    
    for owner_registration in owner_registrations:
        row_num = row_num + 1
        ws.write(row_num, 0, owner_registration['phone'], font_style)
        ws.write(row_num, 1, owner_registration['ownerID'], font_style)
        ws.write(row_num, 2, owner_registration['Name'], font_style)
        ws.write(row_num, 3, owner_registration['shop_list'], font_style)


def get_appointment_data(wb, row_num, date_format, time_format, font_style):
    column_names = ['name', 'contact_number', 'date', 'start_time', 'end_time']
    ws = set_table_header(wb, "appointment_data", column_names, font_style)
    appointments = Appointment.objects.values('name', 'contact_number', 'date', 'start_time', 'end_time')
    
    for appointment in appointments:
        row_num = row_num + 1
        ws.write(row_num, 0, appointment['name'], font_style)
        ws.write(row_num, 1, appointment['contact_number'], font_style)
        ws.write(row_num, 2, appointment['date'], date_format)
        ws.write(row_num, 3, appointment['start_time'], time_format)
        ws.write(row_num, 4, appointment['end_time'], time_format)


def get_services_data(wb, row_num, date_format, time_format, font_style):
    column_names = ['visitID', 'date', 'time', 'shopID', 'ServiceID']
    ws = set_table_header(wb, "Services_data", column_names, font_style)
    services = Services.objects.values('visitID', 'date', 'time', 'shopID', 'ServiceID')
    
    for service in services:
        row_num = row_num + 1
        ws.write(row_num, 0, service['visitID'], font_style)
        ws.write(row_num, 1, service['date'], date_format)
        ws.write(row_num, 2, service['time'], time_format)
        ws.write(row_num, 3, service['shopID'], font_style)
        ws.write(row_num, 4, service['ServiceID'], font_style)


def get_all_services_data(wb, row_num, font_style):
    column_names = ['ServiceID', 'Name']
    ws = set_table_header(wb, "All_Services", column_names, font_style)
    all_services = AllService.objects.values('ServiceID', 'Name')
    
    for service in all_services:
        row_num = row_num + 1
        ws.write(row_num, 0, service['ServiceID'], font_style)
        ws.write(row_num, 1, service['Name'], font_style)


def get_complete_database():
    print('Excel file is getting ready')

    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename='+str(get_current_date())+'-DB.xls'
    
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # set date format
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy-mm-dd'

    #set time format
    time_format = xlwt.XFStyle()
    time_format.num_format_str = 'HH:MM:SS'

    get_client_visit_data(wb, row_num, date_format, time_format, font_style)
    get_membership_data(wb, row_num, date_format, font_style)
    get_expense_data(wb, row_num, date_format, font_style)
    get_shop_registration_data(wb, row_num, font_style)
    get_employee_data(wb, row_num, date_format, font_style)
    get_owner_registration_data(wb, row_num, font_style)
    get_appointment_data(wb, row_num, date_format, time_format, font_style)
    get_services_data(wb, row_num, date_format, time_format, font_style)
    get_all_services_data(wb, row_num, font_style)
    wb.save(response)
    return response