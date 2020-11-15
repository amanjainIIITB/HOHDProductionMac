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
from useraccount.models import OwnerRegistration, Access
from HOHDProductionMac.common_function import atleast_one_shop_registered, set_session, get_list_of_login_user_shops, get_current_date, get_all_membership_based_on_shop_id, \
    convert_date_yyyy_mm_dd_to_dd_mm_yyyy, email_format, is_month_and_year_equal, get_first_shop_name
from HOHDProductionMac.context_processor import get_login_user_shop_details
from fpdf import FPDF
from django.core.files.storage import FileSystemStorage
import cv2
import pdb
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
    return render(request, 'contact_us.html', { "contact_us_image_url": contact_us_image_url})    


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


def employee(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if request.method == "POST":
        employee_id=get_new_employee_id(request)
        print('DOB of the employee')
        print(request.POST.get('DOB'))
        Employee(EmployeeID=employee_id, ShopID=request.session['shop_id'], name=request.POST.get('name'), contact_number=request.POST.get('contact_number'), 
                sex=request.POST.get('sex'), date_of_joining=request.POST.get('date_of_joining'), DOB=request.POST.get('DOB'), 
                position=request.POST.get('position'), temporary_address=request.POST.get('temporary_address'), permanent_address=request.POST.get('permanent_address')).save()
        employee_access = request.POST.get('employee_access')
        if employee_access == "YES":
            if is_employee_account_already_created() == False:
                create_employee_account()
            add_shop_id_to_employee_account()
        print(request)
        print(request.FILES.get('employee_gov_id'))
        if request.FILES.get('employee_gov_id') != None:
            handle_uploaded_file(request, request.FILES.get('employee_gov_id'), employee_id_path, request.session['shop_id'], employee_id)  
        messages.success(request, 'Added successfully', extra_tags='alert')
    employees = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'ShopID', 'sex', 'date_of_joining', 'position', 'DOB', 'temporary_address', 'permanent_address').filter(ShopID=request.session['shop_id'])
    images = get_current_shop_employees(request.session['shop_id'])
    for employee in employees:
        employee['date_of_joining'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(str(employee['date_of_joining']))
        if employee['DOB'] != '':
            employee['DOB'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(str(employee['DOB']))
        if employee['EmployeeID'] in images: 
            employee['govt_id'] = 'images/employee_verification/'+str(request.session['shop_id'])+'/'+ str(employee['EmployeeID']) +'.png'
        else:
            employee['govt_id'] = 'images/not_found.png'
    return render(request, 'employee.html', {'employees': employees})


def update_employee(request, employee_id):
    if request.method == "POST":
        Employee.objects.filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).update(EmployeeID=employee_id, name=request.POST.get('name'),
                       contact_number=request.POST.get('contact_number'),
                       sex=request.POST.get('sex'), date_of_joining=request.POST.get('date_of_joining'), 
                       position=request.POST.get('position'),
                       DOB=request.POST.get('DOB'), temporary_address=request.POST.get('temporary_address'), 
                       permanent_address=request.POST.get('permanent_address'))
        if request.FILES.get('employee_gov_id')!=None:
            handle_uploaded_file(request, request.FILES.get('employee_gov_id'), employee_id_path, request.session['shop_id'], employee_id)  
            messages.success(request, 'Updated successfully', extra_tags='alert')
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/employee/')
    else:
        employee = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'sex', 'date_of_joining', 'position', 'DOB', 'temporary_address', 'permanent_address'). \
            filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).last()
    return render(request, 'update_employee.html', {'employee': employee})


def delete_employee(request, employee_id):
    delete_file(employee_id_path, request.session['shop_id'], employee_id)
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
        return render(request, 'update_expense.html', { 'ExpenseID': expense['ExpenseID'],
                                                        'date': expense['date'],
                                                        'purpose': expense['purpose'],
                                                        'paymentmode': expense['paymentmode'],
                                                        'comment': expense['comment'],
                                                        'amount': expense['amount']})
                                                        

def delete_expense(request, expense_id):
    Expense.objects.filter(shopID=request.session['shop_id'], ExpenseID=expense_id).delete()
    messages.success(request, 'Deleted successfully', extra_tags='alert')
    return redirect('/staff/expense/')


def add_expense(request):
    if request.method == "POST":
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
    return render(request, 'expense.html', r_json)

    
@login_required(login_url="/")
def analysis(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
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
    return render(request, 'aboutus.html',
                  {'shop_name': get_first_shop_name(request)})


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
def download(request, download_type, month, year):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    # put the ip address or dns of your apic-em controller in this url
    url = ''
    if download_type == 'analysis_render' or download_type == 'analysis_excel':
        url = 'http://'+ALLOWED_IP+':8000/staff/getAnalysis/'
    elif download_type == 'expense':
        url = 'http://'+ALLOWED_IP+':8000/staff/getExpense/'
    payload = {"month": int(month), "year": int(year), "shop_id": request.session['shop_id']}
    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the response
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)

    # convert response to json format
    r_json = response.json()
    if download_type == 'analysis_render':
        pdf = render_to_pdf('analysis.html', r_json)
        return HttpResponse(pdf, content_type='application/pdf')
    elif download_type == 'expense':
        return gererate_all_expense_data_for_a_month_in_excel(month, year, r_json)
    elif download_type == 'analysis_excel':
        return gererate_all_customer_data_for_a_month_in_excel(month, year, r_json)


def add_shop_id_in_login_user(request, reg_id, shop_id):
    Access(regID = OwnerRegistration.objects.values('ownerID').filter(phone=request.user.phone).first()['ownerID'], shopID = shopRegistration.ShopID, isowner = True).save()


def add_shop_id_in_entered_user(request, entered_user_name, list_of_shop_id):
    users = OwnerRegistration.objects.values('shop_list').filter(phone=entered_user_name).first()
    shops = ""
    if users['shop_list'] != '':
        shops = users['shop_list']
        for shop_id in list_of_shop_id:
            shops = shops + "," + str(shop_id)
    else:
        shops = list_of_shop_id[0]
        for shop_index in range(1, len(list_of_shop_id)):
            shops = shops + "," + str(list_of_shop_id[shop_index])
    OwnerRegistration.objects.values('shop_list').filter(phone=entered_user_name).update(shop_list=shops)



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
        new_shop_id = get_new_shop_id(request)
        shopRegistration = ShopRegistration()
        shopRegistration.ShopID = new_shop_id
        shopRegistration.Desk_Contact_Number = request.POST.get('Desk_Contact_Number')
        shopRegistration.Shop_Name = request.POST.get('Shop_Name')
        shopRegistration.Shop_Address = request.POST.get('Shop_Address')
        shopRegistration.email = request.POST.get('email')
        shopRegistration.owner_list = OwnerRegistration.objects.values('ownerID').filter(phone=request.user.phone).first()['ownerID']
        add_shop_id_in_entered_user(request, request.user.phone, [shopRegistration.ShopID])
        shopRegistration.save()
        add_shop_id_in_login_user(request, OwnerRegistration.objects.values('ownerID').filter(phone=request.user.phone).first()['ownerID'], shopRegistration.ShopID)
        print(request.FILES.get('logo'))
        if request.FILES.get('logo') != None:
            handle_uploaded_file(request, request.FILES.get('logo'), logo_path, shopRegistration.ShopID, shopRegistration.ShopID) 
        if len(get_list_of_login_user_shops(request)) == 1:
            # check if it is first parlour to be registered then set it as the default parlour
            set_session(request, "shop_id", str(new_shop_id))
        messages.success(request, 'Added successfully', extra_tags='alert')
    print(get_logo_image_url(request))
    return render(request, 'shop_registration.html', {'shop_name': get_first_shop_name(request)})


def edit_parlour(request, shop_id):
    if request.method == "POST":
        ShopRegistration.objects.filter(ShopID=shop_id).update(Desk_Contact_Number=request.POST.get('Desk_Contact_Number'),
        Shop_Name=request.POST.get('Shop_Name'), Shop_Address=request.POST.get('Shop_Address'), email=request.POST.get('email'))
        # pdb.set_trace()
        print(request.FILES.get('logo'))
        if request.FILES.get('logo') != None:
            handle_uploaded_file(request, request.FILES.get('logo'), logo_path, request.session['shop_id'], request.session['shop_id'])
        messages.success(request, 'Updated successfully', extra_tags='alert')
    shop = ShopRegistration.objects.values('ShopID', 'Desk_Contact_Number', 'Shop_Name', 'Shop_Address', 'email').filter(ShopID=shop_id).first()
    set_session(request, "shop_id", shop_id)
    return render(request, 'update_shop.html', {"shop": shop,
                                                'logo_url': get_logo_image_url(request)})


def get_all_owners(request):
    users = OwnerRegistration.objects.all()
    list_users = []
    for userobj in users:
        user = [userobj.get_username(), userobj.get_name(), userobj.get_ownerID(),
                userobj.get_contact_number(), userobj.get_shop_list()]
        list_users.append(user)
    return list_users


def select_parlour(request, shop_id):
    set_session(request, "shop_id", shop_id)
    return redirect('/staff/aboutus/')


def add_owner_id_in_shop_registration_for_entered_user(request, entered_user_name, list_of_shop_id):
    owner = OwnerRegistration.objects.values('ownerID').filter(phone=entered_user_name).first()
    print('Owner data is')
    print(owner)
    for shop_id in list_of_shop_id:
        print(shop_id)
        shopRegistration = ShopRegistration.objects.values('owner_list').filter(ShopID=shop_id).first()
        print(shopRegistration)
        list_of_owners = shopRegistration['owner_list'] + ","+owner['ownerID']
        print(list_of_owners)
        ShopRegistration.objects.values('owner_list').filter(ShopID=shop_id).update(owner_list=list_of_owners)


@login_required(login_url="/")
def add_partner(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if request.method == "POST":
        entered_user_name = request.POST.get('name')
        list_of_shop_id = request.POST.getlist('shop_list[]')
        if len(list_of_shop_id) == 0:
            messages.success(request, 'Select parlour to add', extra_tags='alert')
        else:
            add_shop_id_in_entered_user(request, entered_user_name, list_of_shop_id)
            add_owner_id_in_shop_registration_for_entered_user(request, entered_user_name, list_of_shop_id)
            messages.success(request, 'Selected Parlour Added successfully', extra_tags='alert')
    return render(request, 'add_partner.html', {"shop_details": list(get_login_user_shop_details(request)["shop_details"]),
                                                "list_users": list(get_all_owners(request))})


def save_mem_client_appointment(request):
    membership = Membership.objects.values('Name', 'Contact_Number').filter(shopID=request.session['shop_id'], Contact_Number=request.POST.get('mem_contact_number')).first()
    Appointment(name=membership['Name'], contact_number=membership['Contact_Number'], date=request.POST.get('mem_date'), start_time=request.POST.get('mem_start_time'), end_time=request.POST.get('mem_end_time')).save()
    messages.success(request, 'Appointment Scheduled successfully', extra_tags='alert')
    return redirect('/staff/appointment/')


def save_non_mem_client_appointment(request):
    print(request.POST.get('cust_name'))
    print(request.POST.get('contact_number'))
    print(request.POST.get('date'))
    print(request.POST.get('start_time'))
    print(request.POST.get('end_time'))
    Appointment(name=request.POST.get('cust_name'), contact_number=request.POST.get('contact_number'), date=request.POST.get('date'), start_time=request.POST.get('start_time'), end_time=request.POST.get('end_time')).save()
    messages.success(request, 'Appointment Scheduled successfully', extra_tags='alert')
    return redirect('/staff/appointment/')


def appointment(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
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
    return render(request, 'calendar.html', {'events': list(events), 
                                             "memberships": list(get_all_membership_based_on_shop_id(request, request.session['shop_id']))})
