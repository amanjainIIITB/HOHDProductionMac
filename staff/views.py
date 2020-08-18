from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models.utils import *
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
from useraccount.models import OwnerRegistration
from HOHDProductionMac.common_function import get_month_year_month_name_for_download, atleast_one_shop_registered, \
    get_login_user_shop_details, set_session, get_list_of_login_user_shops, get_current_date, get_all_membership_based_on_shop_id
from fpdf import FPDF
from django.core.files.storage import FileSystemStorage
import cv2

employee_id_path = 'staticfiles/images/employee_verification/'


def get_new_employee_id(request):
    last_employee_id = Employee.objects.values('EmployeeID').filter(ShopID=request.session['shop_id']).last()
    if last_employee_id == None:
        return 'Emp0'
    else:
        new_emplyee_id = 'Emp' + str(int(str(last_employee_id['EmployeeID'])[3:]) + 1)
        return new_emplyee_id


def delete_file(shop_id, employee_id):
    if os.path.exists(str(employee_id_path)+str(shop_id)+'/'+str(employee_id)+'.png'):
        os.remove(str(employee_id_path)+str(shop_id)+'/'+str(employee_id)+'.png')


def handle_uploaded_file(file, shop_id, employee_id):  
    delete_file(shop_id, employee_id)
    if os.path.exists(str(employee_id_path)+str(shop_id)) == False:
        os.mkdir(os.path.join(employee_id_path,shop_id))
    filename, file_extension = os.path.splitext(file.name)
    fs = FileSystemStorage(location=os.path.join(employee_id_path,shop_id)) #defaults to   MEDIA_ROOT  
    filename = fs.save(employee_id+'.png', file)


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
    if request.method == "POST":
        employee_id=get_new_employee_id(request)
        Employee(EmployeeID=employee_id, ShopID=request.session['shop_id'], name=request.POST.get('name'), contact_number=request.POST.get('contact_number'), 
                sex=request.POST.get('sex'), date_of_joining=request.POST.get('date_of_joining'), DOB=request.POST.get('DOB'), 
                position=request.POST.get('position'), temporary_address=request.POST.get('temporary_address'), permanent_address=request.POST.get('permanent_address')).save()
        print(request)
        print(request.FILES.get('employee_gov_id'))
        if request.FILES.get('employee_gov_id') != None:
            handle_uploaded_file(request.FILES.get('employee_gov_id'), request.session['shop_id'], employee_id)  
            filename, file_extension = os.path.splitext(request.FILES.get('employee_gov_id').name)
            if file_extension not in ('jpg', 'jpeg', 'png'):
                messages.success(request, 'Please provide the govt id in jpg, jpeg or png format only', extra_tags='alert')
        messages.success(request, 'Added successfully', extra_tags='alert')
    employees = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'ShopID', 'sex', 'date_of_joining', 'position', 'DOB', 'temporary_address', 'permanent_address').filter(ShopID=request.session['shop_id'])
    images = get_current_shop_employees(request.session['shop_id'])
    for employee in employees:
        if employee['EmployeeID'] in images: 
            employee['govt_id'] = 'images/employee_verification/'+str(request.session['shop_id'])+'/'+ str(employee['EmployeeID']) +'.png'
        else:
            employee['govt_id'] = 'images/not_found.png'
    return render(request, 'employee.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                            'employees': employees,
                                            "shop_details": get_login_user_shop_details(request)})


def update_employee(request, employee_id):
    if request.method == "POST":
        Employee.objects.filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).update(EmployeeID=employee_id, name=request.POST.get('name'),
                       contact_number=request.POST.get('contact_number'),
                       sex=request.POST.get('sex'), date_of_joining=request.POST.get('date_of_joining'), 
                       position=request.POST.get('position'),
                       DOB=request.POST.get('DOB'), temporary_address=request.POST.get('temporary_address'), 
                       permanent_address=request.POST.get('permanent_address'))
        if request.FILES.get('employee_gov_id')!=None:
            filename, file_extension = os.path.splitext(request.FILES.get('employee_gov_id').name)
            if file_extension not in ('.jpg', '.jpeg', '.png'):
                messages.success(request, 'Please provide the govt id in jpg, jpeg or png format only', extra_tags='alert')
            else:
                handle_uploaded_file(request.FILES.get('employee_gov_id'), request.session['shop_id'], employee_id)  
                messages.success(request, 'Updated successfully', extra_tags='alert')
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/employee/')
    else:
        employee = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'sex', 'date_of_joining', 'position', 'DOB', 'temporary_address', 'permanent_address'). \
            filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).last()
    return render(request, 'update_employee.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                    'employee': employee,
                                                    "shop_details": get_login_user_shop_details(request)})


def delete_employee(request, employee_id):
    delete_file(request.session['shop_id'], employee_id)
    Employee.objects.filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).delete()
    # delete_file(request.session['shop_id'], employee_id)
    messages.success(request, 'Deleted successfully', extra_tags='alert')
    return redirect('/staff/employee/')


def format_current_date(date):
    date = str(date).split("-")
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2])).strftime("%B")+" "+date[2]+", "+date[0]


def download_appointment_letter(request, employee_id):
    employee = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'sex', 'date_of_joining', 'position', 'DOB', 'temporary_address', 'permanent_address'). \
            filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).last()
    current_shop_details = ShopRegistration.objects.values('Shop_Name', 'Shop_Address', 'Desk_Contact_Number', 'email').filter(ShopID=request.session['shop_id']).first()
    
    html_template = render_to_string('appointment_letter.html', {'employee': employee, 'current_shop_details': current_shop_details})
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
        return render(request, 'update_expense.html', { "month_year_month_name": get_month_year_month_name_for_download(),
                                                        'ExpenseID': expense['ExpenseID'],
                                                        'date': expense['date'],
                                                        'purpose': expense['purpose'],
                                                        'paymentmode': expense['paymentmode'],
                                                        'comment': expense['comment'],
                                                        'amount': expense['amount'],
                                                        "shop_details": get_login_user_shop_details(request)})

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
    expense_url = 'http://localhost:8000/staff/getExpense/'
    payload = {"month": now.month, "year": now.year, "shop_id": request.session['shop_id']}

    # Content type must be included in the header
    header = {"content-type": "application/json"}
    # Performs a POST on the specified url to get the response
    response = requests.post(expense_url, data=json.dumps(payload), headers=header, verify=False)
    # convert response to json format
    r_json = response.json()
    r_json['month'] = now.month
    r_json['year'] = now.year
    r_json['shop_details'] = get_login_user_shop_details(request)
    return render(request, 'expense.html', r_json)


@login_required(login_url="/")
def analysis(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    now = datetime.datetime.now()

    # put the ip address or dns of your apic-em controller in this url
    expense_url = 'http://localhost:8000/staff/getAnalysis/'
    payload = {"month": now.month, "year": now.year, "shop_id": request.session['shop_id']}

    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the response
    response = requests.post(expense_url, data=json.dumps(payload), headers=header, verify=False)

    # convert response to json format
    r_json = response.json()
    r_json['month'] = now.month
    r_json['year'] = now.year
    r_json['shop_details'] = get_login_user_shop_details(request)
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
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'aboutus.html',
                  {"month_year_month_name": get_month_year_month_name_for_download(),
                  "shop_details": get_login_user_shop_details(request)})


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
    for date in r_json['listOfDates']:
        row_num = row_num + 1
        ws.write(row_num, 0, date, font_style)
        ws.write(row_num, 1, total_amount_of_the_day(date, r_json['dayWiseOnlineOfTheMonth']), font_style)
        ws.write(row_num, 2, total_numberofcustomer_of_the_day(date, r_json['dayWiseOnlineOfTheMonth']), font_style)
        ws.write(row_num, 3, total_amount_of_the_day(date, r_json['dayWiseCashOfTheMonth']), font_style)
        ws.write(row_num, 4, total_numberofcustomer_of_the_day(date, r_json['dayWiseCashOfTheMonth']), font_style)
        ws.write(row_num, 5, int(total_amount_of_the_day(date, r_json['dayWiseOnlineOfTheMonth'])) + 
            int(total_amount_of_the_day(date, r_json['dayWiseCashOfTheMonth'])),font_style)
        ws.write(row_num, 6, int(total_numberofcustomer_of_the_day(date, r_json['dayWiseOnlineOfTheMonth'])) +
            int(total_numberofcustomer_of_the_day(date, r_json['dayWiseCashOfTheMonth'])), font_style)
    wb.save(response)
    return response


@login_required(login_url="/")
def download(request, download_type, month, year):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    # put the ip address or dns of your apic-em controller in this url
    url = ''
    if download_type == 'analysis_render' or download_type == 'analysis_excel':
        url = 'http://localhost:8000/staff/getAnalysis/'
    elif download_type == 'expense':
        url = 'http://localhost:8000/staff/getExpense/'
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
        pdf = render_to_pdf('expense.html', r_json)
        return HttpResponse(pdf, content_type='application/pdf')
    elif download_type == 'analysis_excel':
        return gererate_all_customer_data_for_a_month_in_excel(month, year, r_json)


def add_shop_id_in_login_user(request, shop_id):
    owner_object_values = OwnerRegistration.objects.values('ownerID', 'shop_list'). \
        filter(user=str(request.user.id)).first()
    owner_object = OwnerRegistration.objects.get(ownerID=owner_object_values['ownerID'])
    if owner_object_values['shop_list'] == 'None':
        # if it is first parlour
        owner_object.shop_list = shop_id
    else:
        # if user has already at least one parlour
        owner_object.shop_list = owner_object_values['shop_list'] + ',' + shop_id
    owner_object.save()


def add_shop_id_in_entered_user(request, entered_user_name, list_of_shop_id):
    users = OwnerRegistration.objects.values('shop_list').filter(username=entered_user_name).first()
    shops = ""
    if users['shop_list'] != 'None':
        shops = users['shop_list']
        for shop_id in list_of_shop_id:
            shops = shops + "," + str(shop_id)
    else:
        shops = list_of_shop_id[0]
        for shop_index in range(1, len(list_of_shop_id)):
            shops = shops + "," + str(list_of_shop_id[shop_index])
    OwnerRegistration.objects.values('shop_list').filter(username=entered_user_name).update(shop_list=shops)


def get_new_shop_id(request):
    last_shop_id = ShopRegistration.objects.values('ShopID').last()
    if last_shop_id == None:
        return 'S0'
    else:
        new_shop_id = 'S' + str(int(str(last_shop_id['ShopID'])[1:]) + 1)
        return new_shop_id


@login_required(login_url="/")
def shopreg(request):
    if request.method == "POST":
        shopRegistration = ShopRegistration()
        shopRegistration.ShopID = get_new_shop_id(request)
        shopRegistration.Desk_Contact_Number = request.POST.get('Desk_Contact_Number')
        shopRegistration.Shop_Name = request.POST.get('Shop_Name')
        shopRegistration.Shop_Address = request.POST.get('Shop_Address')
        shopRegistration.email = request.POST.get('email')
        shopRegistration.owner_list = OwnerRegistration.objects.values('ownerID').filter(user=str(request.user.id)).first()['ownerID']
        add_shop_id_in_login_user(request, shopRegistration.ShopID)
        shopRegistration.save()
        if len(get_list_of_login_user_shops(request)) == 1:
            # check if it is first parlour to be registered then set it as the default parlour
            set_session(request, 'S' + str(new_shop_id))
        messages.success(request, 'Added successfully', extra_tags='alert')
    return render(request, 'shop_registration.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                      "shop_details": get_login_user_shop_details(request)})


def edit_parlour(request, shop_id):
    if request.method == "POST":
        ShopRegistration.objects.filter(ShopID=shop_id).update(Desk_Contact_Number=request.POST.get('Desk_Contact_Number'),
        Shop_Name=request.POST.get('Shop_Name'), Shop_Address=request.POST.get('Shop_Address'), email=request.POST.get('email'))
        messages.success(request, 'Updated successfully', extra_tags='alert')
    shop = ShopRegistration.objects.values('ShopID', 'Desk_Contact_Number', 'Shop_Name', 'Shop_Address', 'email').filter(ShopID=shop_id).first()
    set_session(request, shop_id)
    return render(request, 'update_shop.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                            "shop_details": get_login_user_shop_details(request),"shop": shop})


def get_all_owners(request):
    users = OwnerRegistration.objects.all()
    list_users = []
    for userobj in users:
        user = [userobj.get_username().username, userobj.get_name(), userobj.get_ownerID(),
                userobj.get_contact_number(), userobj.get_shop_list()]
        list_users.append(user)
    return list_users


def select_parlour(request, shop_id):
    set_session(request, shop_id)
    return redirect('/staff/aboutus/')


def add_owner_id_in_shop_registration_for_entered_user(request, entered_user_name, list_of_shop_id):
    owner = OwnerRegistration.objects.values('ownerID').filter(username=entered_user_name).first()
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
    return render(request, 'add_partner.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                "shop_details": list(get_login_user_shop_details(request)),
                                                "list_users": list(get_all_owners(request)),
                                                "login_username": request.user.get_username()})


def appointment(request):
    if request.method == 'POST':
        if request.POST.get('mem_contact_number') != None:
            membership = Membership.objects.values('Name', 'Contact_Number').filter(shopID=request.session['shop_id'], Contact_Number=request.POST.get('mem_contact_number')).first()
            Appointment(name=membership['Name'], contact_number=membership['Contact_Number'],
                                    date=request.POST.get('mem_date'), start_time=request.POST.get('mem_start_time'), end_time=request.POST.get('mem_end_time')).save()
        else:
            Appointment(name=request.POST.get('cust_name'), contact_number=request.POST.get('contact_number'), date=request.POST.get('date'), start_time=request.POST.get('start_time'), end_time=request.POST.get('end_time')).save()
    events = Appointment.objects.values('name', 'contact_number', 'date', 'start_time', 'end_time')
    shop_name = ShopRegistration.objects.values('Shop_Name').filter(ShopID=request.session['shop_id']).first()['Shop_Name']
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
    return render(request, 'calendar.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                             "shop_details": get_login_user_shop_details(request),
                                             'events': list(events), 
                                             "membership_based_on_shop_id": list(get_all_membership_based_on_shop_id(request)),   
                                             "login_username": request.user.get_username(),
                                             'shop_name': shop_name})
