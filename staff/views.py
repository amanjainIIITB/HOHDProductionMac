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
from .models import Expense, ShopRegistration
from useraccount.models import OwnerRegistration
from HOHDProductionMac.common_function import get_month_year_month_name_for_download, atleast_one_shop_registered, \
    get_login_user_shop_details, set_session, get_list_of_login_user_shops


def get_new_expense_id(request):
    last_expense_id = Expense.objects.values('ExpenseID').filter(shopID=request.session['shop_id']).last()
    if last_expense_id == None:
        return 'E0'
    else:
        new_expense_id = 'E' + str(int(str(last_expense_id['ExpenseID'])[1:]) + 1)
        return new_expense_id


def update_expense(request, expense_id):
    if request.method == "POST":
        expense = Expense.objects.values('date', 'purpose', 'paymentmode', 'comment', 'amount'). \
            filter(shopID=request.session['shop_id'], ExpenseID=expense_id)
        purpose = request.POST.get('purpose')
        new_amount = int(request.POST.get('amount'))
        if purpose == 'Amount Given':
            new_amount = int(request.POST.get('amount')) * -1
        print('Updated Data in expense' + str(expense))
        expense.update(ExpenseID=expense_id, paymentmode=request.POST.get('paymentmode'),
                       date=request.POST.get('date'), comment=request.POST.get('comment'),
                       purpose=request.POST.get('purpose'), amount=new_amount)
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/expense/')
    else:
        expense = Expense.objects.values('ExpenseID', 'date', 'purpose', 'paymentmode', 'comment', 'amount'). \
            filter(shopID=request.session['shop_id'], ExpenseID=expense_id).last()
        if expense['purpose'] == 'Amount Given':
            expense['amount'] = int(expense['amount']) * -1
        print(expense)
        return render(request, 'update_expense.html', {'ExpenseID': expense['ExpenseID'],
                                                           'date': expense['date'],
                                                           'purpose': expense['purpose'],
                                                           'paymentmode': expense['paymentmode'],
                                                           'comment': expense['comment'],
                                                           'amount': expense['amount']})


def add_expense(request):
    if request.method == "POST":
        expense = Expense()
        expense.ExpenseID = get_new_expense_id(request)
        expense.paymentmode = request.POST.get('paymentmode')
        expense.shopID = request.session['shop_id']
        expense.date = request.POST.get('date')
        expense.comment = request.POST.get('comment')
        expense.purpose = request.POST.get('purpose')
        if expense.purpose == 'Amount Received':
            expense.amount = int(request.POST.get('amount'))
        else:
            expense.amount = int(request.POST.get('amount')) * -1
        expense.save()
        messages.success(request, 'Added successfully', extra_tags='alert')
    return redirect('/staff/expense/')


@login_required(login_url="/useraccount/login/")
def analysis(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    print(request.session['shop_id'])
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
    # print('before sms call')
    # send_sms()
    return render(request, 'analysis.html', r_json)


def send_sms():
    contacts = '9530101150'
    routeid = '50'
    key = '35ED3859DED8C0'
    campaign = '0'
    senderid = 'SMSABS'
    msg = 'Message from the Django Project to the House of Handsomes & Divas'
    url = 'http://sms.autobysms.com/app/smsapi/index.php?key=' + key + '&campaign=' + campaign + '&routeid=' + routeid + \
          '&type=text&contacts=' + contacts + '&senderid=' + senderid + '&msg=' + msg
    response = requests.post(url)


@login_required(login_url="/useraccount/login/")
def expense(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    print(request.session['shop_id'])
    now = datetime.datetime.now()
    # put the ip address or dns of your apic-em controller in this url
    expense_url = 'http://localhost:8000/staff/getExpense/'
    payload = {"month": now.month, "year": now.year, "shop_id": request.session['shop_id']}

    # Content type must be included in the header
    header = {"content-type": "application/json"}
    print('Before response')
    # Performs a POST on the specified url to get the response
    response = requests.post(expense_url, data=json.dumps(payload), headers=header, verify=False)
    print('I am response')
    print(response)
    # convert response to json format
    r_json = response.json()
    r_json['month'] = now.month
    r_json['year'] = now.year
    r_json['shop_details'] = get_login_user_shop_details(request)
    return render(request, 'expense.html', r_json)


def amount(date, datewisedata):
    i = 0
    flag = False
    while i < len(datewisedata):
        # print(date + " " + str(datewisedata[i].get('date')))
        if str(date) == str(datewisedata[i].get('date')):
            return datewisedata[i].get('Amount')
        i = i + 1
    if flag == False:
        return 0


def numberofcustomer(date, datewisedata):
    i = 0
    flag = False
    while i < len(datewisedata):
        # print(date + " " + str(datewisedata[i].get('date')))
        if str(date) == str(datewisedata[i].get('date')):
            return datewisedata[i].get('numberOfCustomer')
        i = i + 1
    if flag == False:
        return 0

@login_required(login_url="/useraccount/login/")
def aboutus(request):
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'aboutus.html',
                  {"month_list": month_year_month_name[0], "year_list": month_year_month_name[2],
                   "month_name": month_year_month_name[1], "shop_details": get_login_user_shop_details(request)})


def gererate_customer_data_in_excel(month, year, r_json):
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
        ws.write(row_num, 1, amount(date, r_json['dayWiseBharatpeOfTheMonth']), font_style)
        ws.write(row_num, 2, numberofcustomer(date, r_json['dayWiseBharatpeOfTheMonth']), font_style)
        ws.write(row_num, 3, amount(date, r_json['dayWisePaytmOfTheMonth']), font_style)
        ws.write(row_num, 4, numberofcustomer(date, r_json['dayWisePaytmOfTheMonth']), font_style)
        ws.write(row_num, 5, amount(date, r_json['dayWiseCashOfTheMonth']), font_style)
        ws.write(row_num, 6, numberofcustomer(date, r_json['dayWiseCashOfTheMonth']), font_style)
        ws.write(row_num, 7, int(amount(date, r_json['dayWiseBharatpeOfTheMonth'])) + int(
            amount(date, r_json['dayWisePaytmOfTheMonth'])) + int(amount(date, r_json['dayWiseCashOfTheMonth'])),
                 font_style)
        ws.write(row_num, 8, int(numberofcustomer(date, r_json['dayWiseBharatpeOfTheMonth'])) + int(
            numberofcustomer(date, r_json['dayWisePaytmOfTheMonth'])) + int(
            numberofcustomer(date, r_json['dayWiseCashOfTheMonth'])), font_style)

    wb.save(response)
    return response


@login_required(login_url="/useraccount/login/")
def download(request, download_type, month, year):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    print(request.session['shop_id'])
    # put the ip address or dns of your apic-em controller in this url
    url = ''
    if download_type == 'analysis_render' or download_type == 'analysis_excel':
        url = 'http://localhost:8000/staff/getAnalysis/'
    elif download_type == 'expense':
        url = 'http://localhost:8000/staff/getExpense/'
    payload = {"month": int(month), "year": int(year), "shop_id": request.session['shop_id']}
    print(payload)
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
        return gererate_customer_data_in_excel(month, year, r_json)


def add_shop_id_in_login_user(request, shop_id):
    owner_object_values = OwnerRegistration.objects.values('ownerID', 'shop_list'). \
        filter(user=str(request.user.id)).first()
    print(owner_object_values)
    owner_object = OwnerRegistration.objects.get(ownerID=owner_object_values['ownerID'])
    print(owner_object)
    if owner_object_values['shop_list'] == 'None':
        owner_object.shop_list = shop_id
    else:
        owner_object.shop_list = owner_object_values['shop_list'] + ',' + shop_id
    owner_object.save()


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
        add_shop_id_in_login_user(request, shopRegistration.ShopID)
        shopRegistration.save()
        if len(get_list_of_login_user_shops(request)) == 1:
            set_session(request, 'S' + str(new_shop_id))
        messages.success(request, 'Added successfully', extra_tags='alert')
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'shop_registration.html', {"month_list": month_year_month_name[0],
                                                      "year_list": month_year_month_name[2],
                                                      "month_name": month_year_month_name[1],
                                                      "shop_details": get_login_user_shop_details(request)})


def get_all_users(request):
    users = OwnerRegistration.objects.all()
    list_users = []
    for userobj in users:
        user = [userobj.get_username().username, userobj.get_name(), userobj.get_ownerID(),
                userobj.get_contact_number(), userobj.get_shop_list()]
        list_users.append(user)
    return list_users


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


def selectparlour(request, shop_id):
    set_session(request, shop_id)
    return redirect('/staff/aboutus/')


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
            messages.success(request, 'Selected Parlour Added successfully', extra_tags='alert')
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'add_partner.html', {"month_list": month_year_month_name[0],
                                                "year_list": month_year_month_name[2],
                                                "month_name": month_year_month_name[1],
                                                "shop_details": get_login_user_shop_details(request),
                                                "list_users": get_all_users(request),
                                                "login_username": request.user.get_username()})
