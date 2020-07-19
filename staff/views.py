from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models.utils import *
import datetime
import requests
import json
import xlwt
from .render_html_to_pdf import render_to_pdf
from .models import Expense, ShopRegistration, Employee
from useraccount.models import OwnerRegistration
from HOHDProductionMac.common_function import get_month_year_month_name_for_download, atleast_one_shop_registered, \
    get_login_user_shop_details, set_session, get_list_of_login_user_shops


def get_new_employee_id(request):
    last_employee_id = Employee.objects.values('EmployeeID').filter(ShopID=request.session['shop_id']).last()
    if last_employee_id == None:
        return 'Emp0'
    else:
        new_emplyee_id = 'Emp' + str(int(str(last_employee_id['EmployeeID'])[3:]) + 1)
        return new_emplyee_id


def employee(request):
    if request.method == "POST":
        Employee(EmployeeID=get_new_employee_id(request), ShopID=request.session['shop_id'], name=request.POST.get('name'), contact_number=request.POST.get('contact_number'), 
                age=request.POST.get('age'), sex=request.POST.get('sex'), date_of_joining=request.POST.get('date_of_joining'), DOB=request.POST.get('DOB'), 
                temporary_address=request.POST.get('temporary_address'), permanent_address=request.POST.get('permanent_address')).save()
        messages.success(request, 'Added successfully', extra_tags='alert')
    employees = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'age', 'sex', 'date_of_joining', 'DOB', 'temporary_address', 'permanent_address').filter(ShopID=request.session['shop_id'])
    return render(request, 'employee.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                            'employees': employees})


def update_employee(request, employee_id):
    if request.method == "POST":
        Employee.objects.filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).update(EmployeeID=employee_id, name=request.POST.get('name'),
                       contact_number=request.POST.get('contact_number'), age=request.POST.get('age'),
                       sex=request.POST.get('sex'), date_of_joining=request.POST.get('date_of_joining'), 
                       DOB=request.POST.get('DOB'), temporary_address=request.POST.get('temporary_address'), 
                       permanent_address=request.POST.get('permanent_address'))
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/employee/')
    else:
        employee = Employee.objects.values('EmployeeID', 'name', 'contact_number', 'age', 'sex', 'date_of_joining', 'DOB', 'temporary_address', 'permanent_address'). \
            filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).last()
    return render(request, 'update_employee.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                    'employee': employee})


def delete_employee(request, employee_id):
    Employee.objects.filter(ShopID=request.session['shop_id'], EmployeeID=employee_id).delete()
    messages.success(request, 'Deleted successfully', extra_tags='alert')
    return redirect('/staff/employee/')


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


@login_required(login_url="/useraccount/login/")
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


@login_required(login_url="/useraccount/login/")
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

@login_required(login_url="/useraccount/login/")
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
    columns = ['Date', 'Bharatpe', 'Bharatpe Customer', 'Paytm', 'Paytm Customer', 'Cash', 'Cash Customer',
               'Total Amount', 'Total Customer']

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    max_length = max(len(r_json['dayWiseBharatpeOfTheMonth']), len(r_json['dayWisePaytmOfTheMonth']),
                     len(r_json['dayWiseCashOfTheMonth']))
    # get your data, from database or from a text file...
    for date in r_json['listOfDates']:
        row_num = row_num + 1
        ws.write(row_num, 0, date, font_style)
        ws.write(row_num, 1, total_amount_of_the_day(date, r_json['dayWiseBharatpeOfTheMonth']), font_style)
        ws.write(row_num, 2, total_numberofcustomer_of_the_day(date, r_json['dayWiseBharatpeOfTheMonth']), font_style)
        ws.write(row_num, 3, total_amount_of_the_day(date, r_json['dayWisePaytmOfTheMonth']), font_style)
        ws.write(row_num, 4, total_numberofcustomer_of_the_day(date, r_json['dayWisePaytmOfTheMonth']), font_style)
        ws.write(row_num, 5, total_amount_of_the_day(date, r_json['dayWiseCashOfTheMonth']), font_style)
        ws.write(row_num, 6, total_numberofcustomer_of_the_day(date, r_json['dayWiseCashOfTheMonth']), font_style)
        ws.write(row_num, 7, int(total_amount_of_the_day(date, r_json['dayWiseBharatpeOfTheMonth'])) + int(
            total_amount_of_the_day(date, r_json['dayWisePaytmOfTheMonth'])) + int(total_amount_of_the_day(date, r_json['dayWiseCashOfTheMonth'])),
                 font_style)
        ws.write(row_num, 8, int(total_numberofcustomer_of_the_day(date, r_json['dayWiseBharatpeOfTheMonth'])) + int(
            total_numberofcustomer_of_the_day(date, r_json['dayWisePaytmOfTheMonth'])) + int(
            total_numberofcustomer_of_the_day(date, r_json['dayWiseCashOfTheMonth'])), font_style)
    wb.save(response)
    return response


@login_required(login_url="/useraccount/login/")
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


@login_required(login_url="/useraccount/login/")
def shopreg(request):
    if request.method == "POST":
        shopRegistration = ShopRegistration()
        shopRegistration.ShopID = get_new_shop_id(request)
        shopRegistration.Desk_Contact_Number = request.POST.get('Desk_Contact_Number')
        shopRegistration.Shop_Name = request.POST.get('Shop_Name')
        shopRegistration.Shop_Address = request.POST.get('Shop_Address')
        shopRegistration.owner_list = OwnerRegistration.objects.values('ownerID').filter(user=str(request.user.id)).first()['ownerID']
        add_shop_id_in_login_user(request, shopRegistration.ShopID)
        shopRegistration.save()
        if len(get_list_of_login_user_shops(request)) == 1:
            # check if it is first parlour to be registered then set it as the default parlour
            set_session(request, 'S' + str(new_shop_id))
        messages.success(request, 'Added successfully', extra_tags='alert')
    return render(request, 'shop_registration.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                      "shop_details": get_login_user_shop_details(request)})


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


@login_required(login_url="/useraccount/login/")
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
                                                "shop_details": get_login_user_shop_details(request),
                                                "list_users": get_all_owners(request),
                                                "login_username": request.user.get_username()})
