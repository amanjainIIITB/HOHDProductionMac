from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models.utils import *
from HOHDProductionMac.settings import ALLOWED_IP
import datetime
import requests
import json
import os
import xlwt
from .render_html_to_pdf import render_to_pdf
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Expense, ShopRegistration, Employee, Appointment
from customer.models import Membership
from useraccount.models import OwnerRegistration, Access, UserManager, User
from useraccount.views import create_owner_registration, get_first_shop_id, get_first_shop_name
from HOHDProductionMac.common_function import atleast_one_shop_registered, set_session, get_list_of_login_user_shops, get_current_date, get_all_membership_based_on_shop_id, \
    convert_date_yyyy_mm_dd_to_dd_mm_yyyy, email_format, is_month_and_year_equal, get_regID, is_page_accessible, get_common_attributes
from HOHDProductionMac.common_function import get_login_user_shop_details, page_display_dict, get_page_permission_dict, get_shop_list_access
from fpdf import FPDF
from django.core.files.storage import FileSystemStorage
import cv2
import calendar


employee_id_path = 'staticfiles/images/employee_verification/'
logo_path = 'staticfiles/images/shop_logo/'
image_not_found = 'images/not_found.png'
contact_us_image_url = 'images/contact_us.jpg'


def contact_us(request):
    if request.method == "POST":
        message_body = 'Info Submitted by You\n'
        message_body = message_body + 'Contact Number: '+request.POST.get('Contact_Number')+'\n'
        message_body = message_body + 'Query: '+request.POST.get('query')+'\n\n'
        message_body = message_body + 'Thank you for Contacting House of Handsomes & Divas, we are reviewing your Query, and we will contact you as soon as possible.\n\n'
        message_body = message_body + 'In the meantime, you can reply to this email if you have more details to add, or you can call our support team, 9530101150.'
        email_format(message_body, 'houseofhandsomes@gmail.com', request.POST.get('email'), 'Customer Support', request.POST.get('Name'))
        messages.success(request, 'Submitted successfully', extra_tags='alert')
    attributes_json = {
        "contact_us_image_url": contact_us_image_url
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'contact_us.html', attributes_json)    


def get_new_employee_id(request):
    last_employee_id = Employee.objects.values('EmployeeID').filter(ShopID=request.session['shop_id']).last()
    if last_employee_id == None:
        return 'Emp0'
    else:
        new_emplyee_id = 'Emp' + str(int(str(last_employee_id['EmployeeID'])[3:]) + 1)
        return new_emplyee_id


def delete_file(base_url, shop_id, employee_id):
    if os.path.exists(str(base_url)+str(shop_id)+'/'+str(employee_id)+'.png'):
        os.remove(str(base_url)+str(shop_id)+'/'+str(employee_id)+'.png')


def handle_uploaded_file(request, file, base_url, shop_id, file_name):  
    filename, file_extension = os.path.splitext(str(file))
    if file_extension not in ('.jpg', '.jpeg', '.png'):
        messages.success(request, 'Please provide the govt id in jpg, jpeg or png format only', extra_tags='alert')
    else:
        delete_file(base_url, shop_id, file_name)
        if os.path.exists(str(base_url)+str(shop_id)) == False:
            os.mkdir(os.path.join(base_url,shop_id))
        filename, file_extension = os.path.splitext(file.name)
        fs = FileSystemStorage(location=os.path.join(base_url,shop_id)) #defaults to   MEDIA_ROOT  
        filename = fs.save(file_name+'.png', file)


def download_employee_govt_id(request, employee_id):
    shop_id = request.session['shop_id']
    employee_govt_id_name = str(employee_id)+'.png'
    if os.path.exists(str(employee_id_path)+str(shop_id)+'/'+str(employee_id)+'.png'):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        filepath = str(employee_id_path)+str(shop_id)+'/'+str(employee_id)+'.png'
        with open((filepath), "rb") as image:
            data = image.read()
        response['Content-Disposition'] = 'attachment; filename="' + str(employee_govt_id_name) +'"'
        response.write(data)
        return response
    else:
        messages.success(request, 'Employee data not found', extra_tags='alert')
        return redirect('/staff/employee/')


def get_current_shop_employees(shop_id):
    if os.path.exists(str(employee_id_path)+str(shop_id)) == False:
        os.mkdir(os.path.join(employee_id_path,shop_id))
    images = []
    for imagename in os.listdir(str(employee_id_path)+str(shop_id)):
        img = cv2.imread(str(employee_id_path)+str(shop_id)+'/'+imagename)
        if img is not None:
            existed_file_name, file_extension = os.path.splitext(imagename)
            images.append(existed_file_name)
    return images


def is_account_exist(contact_number):
    return OwnerRegistration.objects.filter(phone=contact_number).exists()


def is_shop_available_for_account(request, phone):
    return Access.objects.filter(regID=get_regID(request, phone), shopID=request.session['shop_id']).exists()


def create_account(contact_number):
    User.objects.create_user(contact_number, 'hoh1234#')


def remove_shop_access(request, phone):
    if is_shop_available_for_account(request, phone):
        regID = get_regID(request, phone)
        Access.objects.filter(regID=regID).delete()


def update_page_access(request, phone, page_list):
    regID = get_regID(request, phone)
    Access.objects.filter(regID=regID, shopID=request.session['shop_id']).update(page_list=page_list)


def get_page_permissions(request, phone):
    if is_account_exist(phone) and is_shop_available_for_account(request, phone):
        page_permissions = Access.objects.values('page_list').filter(regID=get_regID(request, phone), shopID=request.session['shop_id']).first()['page_list']
        if page_permissions == '':
            return list()
        page_permissions = page_permissions.split(',')
        return [int(i) for i in page_permissions] 
    else:
        return list()


def get_employees_record_for_display(request):
    employees = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'ShopID', 'sex', 'date_of_joining', 'position', 'DOB', 'temporary_address', 'permanent_address', 'access').filter(ShopID=request.session['shop_id'])
    images = get_current_shop_employees(request.session['shop_id'])
    for employee in employees:
        employee['date_of_joining'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(str(employee['date_of_joining']))
        if employee['DOB'] != '':
            employee['DOB'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(str(employee['DOB']))
        if employee['EmployeeID'] in images: 
            employee['govt_id'] = 'images/employee_verification/'+str(request.session['shop_id'])+'/'+ str(employee['EmployeeID']) +'.png'
        else:
            employee['govt_id'] = 'images/not_found.png'
        employee['page_permissions'] = get_page_permissions(request, employee['contact_number'])
    return employees


def create_shop_access_for_newly_added_employee(request, access, phone, page_list):
    if raccess == "YES":
        if is_account_exist(phone) == False:
            create_account(phone)
        add_shop_id_to_user(request, get_regID(request, phone), request.session['shop_id'], False, page_list)


def create_employee(request):
    if is_page_accessible(request, "create_employee") == False:
        return redirect('/staff/aboutus/') 
    employee_id=get_new_employee_id(request)
    page_list = ",".join(request.POST.getlist('page_list[]'))
    Employee(EmployeeID=employee_id, ShopID=request.session['shop_id'], name=request.POST.get('name'), contact_number=request.POST.get('contact_number'), 
            sex=request.POST.get('sex'), date_of_joining=request.POST.get('date_of_joining'), DOB=request.POST.get('DOB'), access = request.POST.get('employee_access'),
            position=request.POST.get('position'), temporary_address=request.POST.get('temporary_address'), permanent_address=request.POST.get('permanent_address')).save()
    create_shop_access_for_newly_added_employee(request, request.POST.get('employee_access'), request.POST.get('contact_number'), page_list)
    if request.FILES.get('employee_gov_id') != None:
        handle_uploaded_file(request, request.FILES.get('employee_gov_id'), employee_id_path, request.session['shop_id'], employee_id)  
    messages.success(request, 'Added successfully', extra_tags='alert')


def employee(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "employee") == False:
        return redirect('/staff/aboutus/') 
    attributes_json = {
        'employees': list(get_employees_record_for_display(request)), 
        'page_display_dict': page_display_dict(),
        'page_permissions': list()
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'employee.html', attributes_json)


def update_employee_access_with_different_phone_number(request, access, phone, page_list):
    remove_shop_access(request, phone)
    if access == "YES":
        add_shop_id_to_user(request, get_regID(request, phone), request.session['shop_id'], False, page_list)

    
def update_employee_access_with_same_phone_number(request, employee, access, phone, page_list):
    # Grant access
    if employee['access'] == "NO" and access == "YES":
        add_shop_id_to_user(request, get_regID(request, phone), request.session['shop_id'], False, page_list)
    # Revoke access
    if employee['access'] == "YES" and access == "NO":
        remove_shop_access(request, phone)
    # In case if we have added or removed access from few of the Pages 
    if employee['access'] == "YES" and access == "YES":
        # check if there is difference in old page access and new submit page access, if yes then update access
        if get_page_permissions(request, employee['contact_number']) != page_list:
            update_page_access(request, phone, page_list)


def update_employee_access(request, employee):
    page_list = ",".join(request.POST.getlist('page_list[]'))
    # if Shop not assigned to the employee simply create the new entry in the Access table
    if request.POST.get('access') == "YES" and is_shop_available_for_account(request, request.POST.get('contact_number')) == False:
        Access(regID=get_regID(request, request.POST.get('contact_number')), shopID=request.session['shop_id'], isowner=False, page_list=page_list).save()
    # in case with shop already assigned but there is some modification in the access
    else:
        if request.POST.get('contact_number') != str(employee['contact_number']):
            update_employee_access_with_different_phone_number(request, request.POST.get('access'), request.POST.get('contact_number'), page_list)
        else:
            update_employee_access_with_same_phone_number(request, employee, request.POST.get('access'), request.POST.get('contact_number'), page_list)


def update_employee(request, employee_id):
    if is_page_accessible(request, "update_employee") == False:
        return redirect('/staff/aboutus/') 
    employee = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'sex', 'date_of_joining', 'position', 'DOB', 'temporary_address', 'permanent_address', 'access').filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).first()
    if request.method == "POST":
        if request.POST.get('access') == "YES" and is_account_exist(request.POST.get('contact_number')) == False:
            create_account(request.POST.get('contact_number'))
            create_owner_registration(request.POST.get('name'), request.POST.get('contact_number'))
        update_employee_access(request, employee)
        Employee.objects.filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).update(EmployeeID=employee_id, name=request.POST.get('name'),
                                access = request.POST.get('access'),
                                contact_number=request.POST.get('contact_number'),
                                sex=request.POST.get('sex'), date_of_joining=request.POST.get('date_of_joining'), 
                                position=request.POST.get('position'),
                                DOB=request.POST.get('DOB'), temporary_address=request.POST.get('temporary_address'), 
                                permanent_address=request.POST.get('permanent_address'))
        if request.FILES.get('employee_gov_id') != None:
            handle_uploaded_file(request, request.FILES.get('employee_gov_id'), employee_id_path, request.session['shop_id'], employee_id)  
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/employee/')
    else:
        employee['page_permissions'] = get_page_permissions(request, employee['contact_number'])
    attributes_json = {
        'employee': employee, 
        'page_display_dict': page_display_dict()
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'update_employee.html', attributes_json)


def delete_employee(request, employee_id):
    if is_page_accessible(request, "delete_employee") == False:
        return redirect('/staff/aboutus/') 
    employee = Employee.objects.values('access', 'contact_number').filter(EmployeeID=employee_id).first()
    if employee['access'] == "yes":
        remove_shop_access(request, employee['contact_number'])
    delete_file(employee_id_path, request.session['shop_id'], employee_id)
    remove_shop_access(request, employee['contact_number'])
    Employee.objects.filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).delete()
    messages.success(request, 'Deleted successfully', extra_tags='alert')
    return redirect('/staff/employee/')


def format_current_date(date):
    date = str(date).split("-")
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2])).strftime("%B")+" "+date[2]+", "+date[0]


def download_appointment_letter(request, employee_id):
    employee = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'sex', 'date_of_joining', 'position', 'DOB', 'temporary_address', 'permanent_address'). \
            filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).last()
    current_shop_details = ShopRegistration.objects.values('Shop_Name', 'Shop_Address', 'Desk_Contact_Number', 'email').filter(ShopID=request.session['shop_id']).first()
    
    html_template = render_to_string('appointment_letter.html', {'employee': employee, 'current_shop_details': current_shop_details, 'logo_url': get_logo_image_url(request),})
    pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="appointment_letter.pdf"'
    return response

    # return render(request, 'appointment_letter.html', {'employee': employee, 'current_shop_details': current_shop_details})


def get_new_expense_id(request):
    last_expense_id = Expense.objects.values('ExpenseID').filter(shopID=request.session['shop_id']).last()
    if last_expense_id == None:
        return 'E0'
    else:
        new_expense_id = 'E' + str(int(str(last_expense_id['ExpenseID'])[1:]) + 1)
        return new_expense_id


def update_expense(request, expense_id):
    if is_page_accessible(request, "update_expense") == False:
        return redirect('/staff/aboutus/') 
    if request.method == "POST":
        new_amount = int(request.POST.get('amount'))
        if request.POST.get('purpose') == 'Amount Given':
            new_amount = int(request.POST.get('amount')) * -1
        Expense.objects.filter(shopID=request.session['shop_id'], ExpenseID=expense_id).update(ExpenseID=expense_id, paymentmode=request.POST.get('paymentmode'),
                       date=request.POST.get('date'), comment=request.POST.get('comment'),
                       purpose=request.POST.get('purpose'), amount=new_amount)
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/expense/')
    else:
        expense = Expense.objects.values('ExpenseID', 'date', 'purpose', 'paymentmode', 'comment', 'amount'). \
            filter(shopID=request.session['shop_id'], ExpenseID=expense_id).last()
        if expense['purpose'] == 'Amount Given':
            expense['amount'] = int(expense['amount']) * -1
        attributes_json = {
            'ExpenseID': expense['ExpenseID'],
            'date': expense['date'],
            'purpose': expense['purpose'],
            'paymentmode': expense['paymentmode'],
            'comment': expense['comment'],
            'amount': expense['amount']
        }
        get_common_attributes(request, attributes_json)
        return render(request, 'update_expense.html', attributes_json)
                                                        

def delete_expense(request, expense_id):
    if is_page_accessible(request, "delete_expense") == False:
        return redirect('/staff/aboutus/') 
    Expense.objects.filter(shopID=request.session['shop_id'], ExpenseID=expense_id).delete()
    messages.success(request, 'Deleted successfully', extra_tags='alert')
    return redirect('/staff/expense/')


def add_expense(request):
    if is_page_accessible(request, "add_expense") == False:
        return redirect('/staff/aboutus/') 
    if request.POST.get('purpose') == 'Amount Received':
        expense.amount = int(request.POST.get('amount'))
    else:
        expense.amount = int(request.POST.get('amount')) * -1
    Expense(ExpenseID=get_new_expense_id(request), paymentmode=request.POST.get('paymentmode'), shopID=request.session['shop_id'], date=request.POST.get('date'), 
            comment=request.POST.get('comment'), purpose=request.POST.get('purpose'), amount=expense.amount).save()
    messages.success(request, 'Added successfully', extra_tags='alert')
    return redirect('/staff/expense/')


@login_required(login_url="/")
def expense(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "expense") == False:
        return redirect('/staff/aboutus/') 
    now = datetime.datetime.now()
    # put the ip address or dns of your apic-em controller in this url
    expense_url = 'http://'+ALLOWED_IP+':8000/staff/getExpense/'
    payload = {"month": now.month, "year": now.year, "shop_id": request.session['shop_id']}

    # Content type must be included in the header
    header = {"content-type": "application/json"}
    # Performs a POST on the specified url to get the response
    response = requests.post(expense_url, data=json.dumps(payload), headers=header, verify=False)
    # convert response to json format
    r_json = response.json()
    r_json['month'] = now.month
    r_json['year'] = now.year
    get_common_attributes(request, r_json)
    return render(request, 'expense.html', r_json)

    
@login_required(login_url="/")
def analysis(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "analysis") == False:
        return redirect('/staff/aboutus/') 
    now = datetime.datetime.now()

    # put the ip address or dns of your apic-em controller in this url
    expense_url = 'http://'+ALLOWED_IP+':8000/staff/getAnalysis/'
    payload = {"month": now.month, "year": now.year, "shop_id": request.session['shop_id']}

    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the response
    response = requests.post(expense_url, data=json.dumps(payload), headers=header, verify=False)

    # convert response to json format
    r_json = response.json()
    r_json['month'] = now.month
    r_json['year'] = now.year
    get_common_attributes(request, r_json)
    return render(request, 'analysis.html', r_json)


def total_amount_of_the_day(date, datewisedata):
    i = 0
    flag = False
    while i < len(datewisedata):
        if str(date) == str(datewisedata[i].get('date')):
            return datewisedata[i].get('Amount')
        i = i + 1
    if flag == False:
        return 0


def total_numberofcustomer_of_the_day(date, datewisedata):
    i = 0
    flag = False
    while i < len(datewisedata):
        if str(date) == str(datewisedata[i].get('date')):
            return datewisedata[i].get('numberOfCustomer')
        i = i + 1
    if flag == False:
        return 0


@login_required(login_url="/")
def aboutus(request):
    attributes_json = {}
    get_common_attributes(request, attributes_json)
    return render(request, 'aboutus.html', attributes_json)


def gererate_all_customer_data_for_a_month_in_excel(month, year, r_json):
    print('Excel file is getting ready')
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename=' + year + '-' + month + '-analysis.xls'

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # adding sheet
    ws = wb.add_sheet("customer_data")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['Date', 'Online', 'Online Customer', 'Cash', 'Cash Customer', 'Total Amount', 'Total Customer']


    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    max_length = max(len(r_json['dayWiseOnlineOfTheMonth']), len(r_json['dayWiseCashOfTheMonth']))
    # get your data, from database or from a text file...

    total_amount = 0
    total_number_of_customer = 0
    total_online_amount = 0
    total_online_number_of_customer = 0
    total_cash_amount = 0
    total_cash_number_of_customer = 0

    for date in r_json['listOfDates']:
        row_num = row_num + 1
        ws.write(row_num, 0, date, font_style)
        val = total_amount_of_the_day(date, r_json['dayWiseOnlineOfTheMonth'])
        total_online_amount = total_online_amount + val
        ws.write(row_num, 1, val, font_style)
        val = total_numberofcustomer_of_the_day(date, r_json['dayWiseOnlineOfTheMonth'])
        total_online_number_of_customer = total_online_number_of_customer + val
        ws.write(row_num, 2, val, font_style)
        val = total_amount_of_the_day(date, r_json['dayWiseCashOfTheMonth'])
        total_cash_amount = total_cash_amount + val
        ws.write(row_num, 3, val, font_style)
        val = total_numberofcustomer_of_the_day(date, r_json['dayWiseCashOfTheMonth'])
        total_cash_number_of_customer = total_cash_number_of_customer + val
        ws.write(row_num, 4, val, font_style)
        val = int(total_amount_of_the_day(date, r_json['dayWiseOnlineOfTheMonth'])) + int(total_amount_of_the_day(date, r_json['dayWiseCashOfTheMonth']))
        total_amount = total_amount + val
        ws.write(row_num, 5, val,font_style)
        val = int(total_numberofcustomer_of_the_day(date, r_json['dayWiseOnlineOfTheMonth'])) + int(total_numberofcustomer_of_the_day(date, r_json['dayWiseCashOfTheMonth']))
        total_number_of_customer = total_number_of_customer + val
        ws.write(row_num, 6, val, font_style)
    
    ws.write(row_num+2, 0, 'Total', font_style)
    ws.write(row_num+2, 1, total_online_amount, font_style)
    ws.write(row_num+2, 2, total_online_number_of_customer, font_style)
    ws.write(row_num+2, 3, total_cash_amount, font_style)
    ws.write(row_num+2, 4, total_cash_number_of_customer, font_style)
    ws.write(row_num+2, 5, total_amount, font_style)
    ws.write(row_num+2, 6, total_number_of_customer, font_style)
    wb.save(response)
    return response


def write_static_data_in_expense_excel(ws, row_num, date, purpose, comment, payment_mode, amount):
    ws.write(row_num, 0, date)
    ws.write(row_num, 1, purpose)
    ws.write(row_num, 2, comment)
    ws.write(row_num, 3, payment_mode)
    ws.write(row_num, 4, amount)
    return ws
    


def gererate_all_expense_data_for_a_month_in_excel(month, year, r_json):
    print('Excel file is getting ready')
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename=' + year + '-' + month + '-expense.xls'

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # adding sheet
    ws = wb.add_sheet("expense_data")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['Date', 'Purpose', 'Comment', 'Payment Mode', 'Amount']

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    print(calendar.monthrange(2012,1)[1])
    for obj in r_json['sell_of_the_month']:
        row_num = row_num + 1
        if is_month_and_year_equal(str(datetime.date(int(year), int(month), 1)), str(datetime.date.today())):
            ws = write_static_data_in_expense_excel(ws, row_num, obj[0], obj[1], obj[2], obj[3], obj[4])
        else:
            day = calendar.monthrange(int(year), int(month))[1]
            date = str(datetime.date(year=int(year), month=int(month), day=day))
            ws = write_static_data_in_expense_excel(ws, row_num, date, obj[1], obj[2], obj[3], obj[4])

    for obj in r_json['expense']:
        row_num = row_num + 1
        ws = write_static_data_in_expense_excel(ws, row_num, obj['date'], obj['purpose'], obj['comment'], obj['paymentmode'], obj['amount'])

    for obj in r_json['remaining_balance']:
        row_num = row_num + 1
        if is_month_and_year_equal(str(datetime.date(int(year), int(month), 1)), str(datetime.date.today())):
            ws = write_static_data_in_expense_excel(ws, row_num, obj[0], obj[1], obj[2], obj[3], obj[4])
        else:
            day = calendar.monthrange(int(year), int(month))[1]
            date = str(datetime.date(year=int(year), month=int(month), day=day))
            ws = write_static_data_in_expense_excel(ws, row_num, date, obj[1], obj[2], obj[3], obj[4])
    wb.save(response)
    return response


@login_required(login_url="/")
def download_analysis_report(request, month, year):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "download_analysis_report") == False:
        return redirect('/staff/aboutus/') 
    url = 'http://'+ALLOWED_IP+':8000/staff/getAnalysis/'
    payload = {"month": int(month), "year": int(year), "shop_id": request.session['shop_id']}
    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the response
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    pdf = render_to_pdf('analysis.html', response.json())
    return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url="/")
def download_expense_data(request, month, year):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "download_expense_data") == False:
        return redirect('/staff/aboutus/') 
    url = 'http://'+ALLOWED_IP+':8000/staff/getExpense/'
    payload = {"month": int(month), "year": int(year), "shop_id": request.session['shop_id']}
    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the response
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    return gererate_all_expense_data_for_a_month_in_excel(month, year, response.json())


@login_required(login_url="/")
def download_customer_data(request, month, year):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "download_customer_data") == False:
        return redirect('/staff/aboutus/') 
    url = 'http://'+ALLOWED_IP+':8000/staff/getAnalysis/'
    payload = {"month": int(month), "year": int(year), "shop_id": request.session['shop_id']}
    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the response
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    return gererate_all_customer_data_for_a_month_in_excel(month, year, response.json())


def get_add_shop_id_to_user_report(request, regID, shop_id, isowner, page_list):
    access_report = {
        'Name of the Report' : 'add_shop_id_to_user',
        'regID' : regID,
        'shop_id' : shop_id,
        '(Are you Owner)isowner' : isowner,
        'page_list' : page_list
    }
    print(access_report)


def add_shop_id_to_user(request, reg_id, shop_id, isowner, page_list):
    get_add_shop_id_to_user_report(request, reg_id, shop_id, isowner, page_list)
    Access(regID = reg_id, shopID = shop_id, isowner = isowner, page_list=page_list).save()


def add_shop_id_in_entered_user(request, entered_contact_number, list_of_shop_id):
    for shop_id in list_of_shop_id:
        add_shop_id_to_user(request, get_regID(request, entered_contact_number), shop_id, True, '')


def get_new_shop_id(request):
    last_shop_id = ShopRegistration.objects.values('ShopID').last()
    if last_shop_id == None:
        return 'S0'
    else:
        new_shop_id = 'S' + str(int(str(last_shop_id['ShopID'])[1:]) + 1)
        return new_shop_id


def get_logo_image_url(request):
    shop_id = request.session['shop_id']
    if os.path.exists(str(logo_path)+str(shop_id)+'/'+str(shop_id)+'.png'):
        return 'images/shop_logo/'+str(shop_id)+'/'+str(shop_id)+'.png'
    else:
        return image_not_found


@login_required(login_url="/")
def shopreg(request):
    if request.method == "POST":

        # New SHop Details and save it 
        new_shop_id = get_new_shop_id(request)
        shopRegistration = ShopRegistration()
        shopRegistration.ShopID = new_shop_id
        shopRegistration.Desk_Contact_Number = request.POST.get('Desk_Contact_Number')
        shopRegistration.Shop_Name = request.POST.get('Shop_Name')
        shopRegistration.Shop_Address = request.POST.get('Shop_Address')
        shopRegistration.email = request.POST.get('email')
        shopRegistration.save()

        # Provide access to the shop whoever is registering shop.
        add_shop_id_to_user(request, OwnerRegistration.objects.values('ownerID').filter(phone=request.user.phone).first()['ownerID'], shopRegistration.ShopID, True, '')
        
        # Set shop_list_access session so that at least the user who has registered new shop can access it without logout and login again
        set_session(request, "shop_list_access", get_shop_list_access(request.session['regID']))
        
        # Set shop_details session to appear the added shop in the list of shops in parlour list
        set_session(request, "shop_details", get_login_user_shop_details(request))

        # Check if user has upload logo of the shop then only handle it
        if request.FILES.get('logo') != None:
            handle_uploaded_file(request, request.FILES.get('logo'), logo_path, shopRegistration.ShopID, shopRegistration.ShopID) 
        
        # If it's the first shop in user accound then set shop_id and shop_name
        if len(get_list_of_login_user_shops(request)) == 1:
            # check if it is first parlour to be registered then set it as the default parlour
            set_session(request, "shop_id", str(new_shop_id))
            set_session(request, "shop_name", str(shopRegistration.Shop_Name))

        messages.success(request, 'Added successfully', extra_tags='alert')
    attributes_json = {}
    get_common_attributes(request, attributes_json)
    return render(request, 'shop_registration.html', attributes_json)


def edit_parlour(request, shop_id):
    if is_page_accessible(request, "edit_parlour") == False:
        return redirect('/staff/aboutus/') 
    if request.method == "POST":
        ShopRegistration.objects.filter(ShopID=shop_id).update(Desk_Contact_Number=request.POST.get('Desk_Contact_Number'),
        Shop_Name=request.POST.get('Shop_Name'), Shop_Address=request.POST.get('Shop_Address'), email=request.POST.get('email'))
        # pdb.set_trace()
        print(request.FILES.get('logo'))
        if request.FILES.get('logo') != None:
            handle_uploaded_file(request, request.FILES.get('logo'), logo_path, request.session['shop_id'], request.session['shop_id'])
        messages.success(request, 'Updated successfully', extra_tags='alert')
    shop = ShopRegistration.objects.values('ShopID', 'Desk_Contact_Number', 'Shop_Name', 'Shop_Address', 'email').filter(ShopID=shop_id).first()
    set_session(request, "shop_id", get_first_shop_id(request.session['regID']))
    set_session(request, "shop_name", get_first_shop_name(request))
    set_session(request, "shop_details", get_login_user_shop_details(request))
    set_session(request, "shop_list_access", get_shop_list_access(request.session['regID']))
    #Need to set shop name, shop_details, access
    attributes_json = {
        "shop": shop,
        'logo_url': get_logo_image_url(request)
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'update_shop.html', attributes_json)


def get_all_owners(request):
    users = OwnerRegistration.objects.all()
    list_users = []
    for userobj in users:
        user = [userobj.get_username(), userobj.get_name(), userobj.get_ownerID(),
                userobj.get_contact_number()]
        list_users.append(user)
    return list_users


def select_parlour(request, shop_id):
    set_session(request, "shop_id", shop_id)
    return redirect('/staff/aboutus/')


@login_required(login_url="/")
def add_partner(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "add_partner") == False:
        return redirect('/staff/aboutus/') 
    if request.method == "POST":
        entered_contact_number = request.POST.get('contact_number')
        list_of_shop_id = request.POST.getlist('shop_list[]')
        if len(list_of_shop_id) == 0:
            messages.success(request, 'Select parlour to add', extra_tags='alert')
        else:
            add_shop_id_in_entered_user(request, entered_contact_number, list_of_shop_id)
            messages.success(request, 'Selected Parlour Added successfully', extra_tags='alert')
    attributes_json = {
        "shop_details": list(get_login_user_shop_details(request)),
        "list_users": list(get_all_owners(request))
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'add_partner.html', attributes_json)


def save_mem_client_appointment(request):
    if is_page_accessible(request, "save_mem_client_appointment") == False:
        return redirect('/staff/aboutus/') 
    membership = Membership.objects.values('Name', 'Contact_Number').filter(shopID=request.session['shop_id'], Contact_Number=request.POST.get('mem_contact_number')).first()
    Appointment(name=membership['Name'], contact_number=membership['Contact_Number'], date=request.POST.get('mem_date'), start_time=request.POST.get('mem_start_time'), end_time=request.POST.get('mem_end_time')).save()
    messages.success(request, 'Appointment Scheduled successfully', extra_tags='alert')
    return redirect('/staff/appointment/')


def save_non_mem_client_appointment(request):
    if is_page_accessible(request, "save_non_mem_client_appointment") == False:
        return redirect('/staff/aboutus/') 
    Appointment(name=request.POST.get('cust_name'), contact_number=request.POST.get('contact_number'), date=request.POST.get('date'), start_time=request.POST.get('start_time'), end_time=request.POST.get('end_time')).save()
    messages.success(request, 'Appointment Scheduled successfully', extra_tags='alert')
    return redirect('/staff/appointment/')


def appointment(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "appointment") == False:
        return redirect('/staff/aboutus/') 
    events = Appointment.objects.values('name', 'contact_number', 'date', 'start_time', 'end_time')
    for event in events:
        event['day'] = event['date'].day
        event['month'] = event['date'].month
        event['year'] = event['date'].year
        event['date'] = str(event['date'])
        event['start_hour'] = event['start_time'].hour
        event['start_minute'] = event['start_time'].minute
        event['end_hour'] = event['end_time'].hour
        event['end_minute'] = event['end_time'].minute
        event['start_time'] = str(event['start_time'])
        event['end_time'] = str(event['end_time'])
    attributes_json = {
        'events': list(events), 
        "memberships": list(get_all_membership_based_on_shop_id(request, request.session['shop_id']))
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'calendar.html', attributes_json)
