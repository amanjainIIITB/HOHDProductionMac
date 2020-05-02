from django.shortcuts import render, redirect
from django.db.models import Sum
from customer.models import *
from .models import Expense, ShopRegistration
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.utils import *
from .render_html_to_pdf import render_to_pdf
import requests
import json
import xlwt

def storeExpense(request):
    expense = Expense()
    expense.paymentmode = request.POST.get('paymentmode')
    expense.date = request.POST.get('date')
    expense.comment = request.POST.get('comment')
    expense.purpose = request.POST.get('purpose')
    if expense.purpose == 'Cash Received':
        expense.amount = int(request.POST.get('amount'))
    else:
        expense.amount = int(request.POST.get('amount'))*-1
    expense.save()
    messages.success(request, 'Added successfully', extra_tags='alert')
    return redirect('/staff/expense/')


def prepareDefaultDB(tablename, bardate, time):
    customer=''
    if(tablename=='Bharatpe'):
        customer = BharatPe()
    elif(tablename=='Paytm'):
        customer = Paytm()
    elif(tablename == 'Cash'):
        customer = client()
    customer.date = bardate
    customer.bardate = bardate
    customer.time = time
    customer.numberofclient = 0
    customer.amount = 0
    customer.save()


def get_last_6_month_data_for_bar_graph(year, month):
    now = datetime.datetime.now()
    barGraphNumberOfMonth = 6
    revenueBarGraphData = []
    month_list = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    bharatpe_obj = BharatPe.objects.all().filter().values('bardate').annotate(Amount=Sum('amount'),numberOfCustomer=Sum('numberofclient')).order_by('-bardate')
    bharatpe_map = {}
    for obj in bharatpe_obj:
        bharatpe_map[str(obj['bardate'])] = [obj['Amount'], obj['numberOfCustomer']]

    paytm_obj = Paytm.objects.all().filter().values('bardate').annotate(Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('-bardate')
    paytm_map = {}
    for obj in paytm_obj:
        paytm_map[str(obj['bardate'])] = [obj['Amount'], obj['numberOfCustomer']]

    cash_obj = client.objects.all().filter().values('bardate').annotate(Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('-bardate')
    cash_map = {}
    for obj in cash_obj:
        cash_map[str(obj['bardate'])] = [obj['Amount'], obj['numberOfCustomer']]

    for index in range(barGraphNumberOfMonth):
        month = month - 1
        if month==-1:
            month = 11
            year = year - 1
        date = str(datetime.datetime(year, month+1, 1).strftime('%Y-%m-%d'))
        amount = 0
        numberofcustomer = 0
        if date in bharatpe_map.keys():
            amount = amount + bharatpe_map[date][0]
            numberofcustomer = numberofcustomer + bharatpe_map[date][1]
        if date in paytm_map.keys():
            amount = amount + paytm_map[date][0]
            numberofcustomer = numberofcustomer + paytm_map[date][1]
        if date in cash_map.keys():
            amount = amount + cash_map[date][0]
            numberofcustomer = numberofcustomer + cash_map[date][1]

        revenueBarGraphData.append([month_list[month], amount, numberofcustomer])
    return revenueBarGraphData


def prepare_list_of_dates(year, month):
    now = datetime.datetime.now()
    number_of_days = 0
    if month==now.month:
        number_of_days = datetime.datetime.today().day
    else:
        if(month==12):
            number_of_days = (datetime.datetime(year+1, 1, 1) - datetime.datetime(year, month, 1)).days
        else:
            number_of_days = (datetime.datetime(year, month+1, 1) - datetime.datetime(year, month, 1)).days
    listOfDates = []
    day = 1
    while (day <= number_of_days):
        listOfDates.append(datetime.date(day=day, month=month, year=year).strftime('%Y-%m-%d'))
        day = day + 1
    return listOfDates

# @login_required(login_url="/useraccount/login/")
def analysis(request):

    now = datetime.datetime.now()

    # put the ip address or dns of your apic-em controller in this url
    expense_url = 'http://localhost:8000/staff/getAnalysis/'
    payload = {"month": now.month, "year": now.year}

    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the response
    response = requests.post(expense_url, data=json.dumps(payload), headers=header, verify=False)

    # convert response to json format
    r_json = response.json()
    r_json['month'] = now.month
    r_json['year'] = now.year
    return render(request, 'analysis.html', r_json)

def generate_month_year_month_name_for_download():
    month_list = []
    year_list = []
    month_name = []
    number_to_month_name = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov',
                            'Dec']
    current_month = now.month
    current_year = now.year
    for i in range(4):
        if current_month == 0:
            current_month = 12
            current_year = current_year - 1
        month_list.append(current_month)
        month_name.append(number_to_month_name[current_month - 1])
        year_list.append(current_year)
        current_month = current_month - 1
    return [month_list, year_list, month_name]

class AnalysisReport(APIView):
    def get(self):
        pass

    def post(self, request):
        # get current date and time
        now = datetime.datetime.now()
        month = request.data['month']
        year = request.data['year']
        bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')

        dayWisePaytmOfTheMonth = Paytm.objects.all().filter(bardate=bardate).values('date').annotate(
            Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('date')
        dayWiseBharatpeOfTheMonth = BharatPe.objects.all().filter(bardate=bardate).values('date').annotate(
            Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('date')
        dayWiseCashOfTheMonth = client.objects.all().filter(bardate=bardate).values('date').annotate(
            Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('date')

        total_Paytm_amount_Of_The_Month = Paytm.objects.filter(bardate=bardate).aggregate(Sum('amount'))
        total_Bharatpe_amount_Of_The_Month = BharatPe.objects.filter(bardate=bardate).aggregate(Sum('amount'))
        if total_Paytm_amount_Of_The_Month['amount__sum'] == None:
            # prepareDefaultDB('Paytm', bardate, now.strftime('%H:%M:%S'))
            total_Paytm_amount_Of_The_Month['amount__sum'] = 0
        if total_Bharatpe_amount_Of_The_Month['amount__sum'] == None:
            # prepareDefaultDB('Bharatpe', bardate, now.strftime('%H:%M:%S'))
            total_Bharatpe_amount_Of_The_Month['amount__sum'] = 0
        total_online_amount_Of_The_Month = total_Paytm_amount_Of_The_Month['amount__sum'] + \
                                           total_Bharatpe_amount_Of_The_Month['amount__sum']
        total_cash_amount_Of_The_Month = client.objects.filter(bardate=bardate).aggregate(Sum('amount'))
        if total_cash_amount_Of_The_Month['amount__sum'] == None:
            # prepareDefaultDB('Cash', bardate, now.strftime('%H:%M:%S'))
            total_cash_amount_Of_The_Month['amount__sum'] = 0

        number_of_Paytm_customer_Of_The_Month = Paytm.objects.filter(bardate=bardate).aggregate(Sum('numberofclient'))
        number_of_Bharatpe_customer_Of_The_Month = BharatPe.objects.filter(bardate=bardate).aggregate(Sum('numberofclient'))
        number_of_cash_customer_Of_The_Month = client.objects.filter(bardate=bardate).aggregate(Sum('numberofclient'))

        if number_of_Paytm_customer_Of_The_Month['numberofclient__sum'] == None:
            number_of_Paytm_customer_Of_The_Month['numberofclient__sum'] = 0
        if number_of_Bharatpe_customer_Of_The_Month['numberofclient__sum'] == None:
            number_of_Bharatpe_customer_Of_The_Month['numberofclient__sum'] = 0
        if number_of_cash_customer_Of_The_Month['numberofclient__sum'] == None:
            number_of_cash_customer_Of_The_Month['numberofclient__sum'] = 0

        number_of_online_customer_Of_The_Month = number_of_Paytm_customer_Of_The_Month['numberofclient__sum'] + \
                                                 number_of_Bharatpe_customer_Of_The_Month['numberofclient__sum']

        month_list = []
        year_list = []
        month_name = []
        number_to_month_name = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov',
                                'Dec']
        current_month = now.month
        current_year = now.year
        for i in range(4):
            if current_month == 0:
                current_month = 12
                current_year = current_year - 1
            month_list.append(current_month)
            month_name.append(number_to_month_name[current_month - 1])
            year_list.append(current_year)
            current_month = current_month - 1
        print(month_list)
        print(month_name)
        print(year_list)

        return Response({'revenueBarGraphData': get_last_6_month_data_for_bar_graph(year, month),
                        'dayWiseBharatpeOfTheMonth': dayWiseBharatpeOfTheMonth,
                        'dayWisePaytmOfTheMonth': dayWisePaytmOfTheMonth,
                        'dayWiseCashOfTheMonth': dayWiseCashOfTheMonth,
                        'listOfDates': prepare_list_of_dates(year, month),
                        'total_cash_amount_Of_The_Month': total_cash_amount_Of_The_Month['amount__sum'],
                        'total_online_amount_Of_The_Month': total_online_amount_Of_The_Month,
                        'number_of_cash_customer_Of_The_Month': number_of_cash_customer_Of_The_Month['numberofclient__sum'],
                        'number_of_online_customer_Of_The_Month': number_of_online_customer_Of_The_Month,
                        'month_list': month_list,
                        'year_list': year_list,
                        'month_name': month_name })


# """
# It will remove all the entries which has 0 amount
# """
# def cleanDB():
#     BharatPe.objects.filter(amount=0).delete()
#     Paytm.objects.filter(amount=0).delete()
#     client.objects.filter(amount=0).delete()

# @login_required(login_url="/useraccount/login/")
def expense(request):
    # cleanDB()

    now = datetime.datetime.now()
    # put the ip address or dns of your apic-em controller in this url
    expense_url = 'http://localhost:8000/staff/getExpense/'
    payload = {"month":now.month, "year":now.year}

    # Content type must be included in the header
    header = {"content-type": "application/json"}

    print('hello')
    print(payload)
    # Performs a POST on the specified url to get the response
    response = requests.post(expense_url, data=json.dumps(payload), headers=header, verify=False)

    print('response')
    print(response)
    # convert response to json format
    r_json = response.json()
    r_json['month'] = now.month
    r_json['year'] = now.year
    return render(request, 'expense.html',r_json)

def get_month_year_month_name_for_download():
    now = datetime.datetime.now()
    month_year_month_name = []
    month_list = []
    year_list = []
    month_name = []
    number_to_month_name = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov',
                            'Dec']
    current_month = now.month
    current_year = now.year
    for i in range(4):
        if current_month == 0:
            current_month = 12
            current_year = current_year - 1
        month_list.append(current_month)
        month_name.append(number_to_month_name[current_month - 1])
        year_list.append(current_year)
        current_month = current_month - 1
    month_year_month_name.append(month_list)
    month_year_month_name.append(month_name)
    month_year_month_name.append(year_list)
    return month_year_month_name

class ExpenseReport(APIView):
    def get(self):
        pass
    def post(self, request):
        print('hey')
        month=request.data['month']
        print(request.data['year'])
        year=request.data['year']
        bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
        total_Paytm_amount_Of_The_Month = Paytm.objects.filter(bardate=bardate).aggregate(Sum('amount'))
        total_BharatPe_amount_Of_The_Month = BharatPe.objects.filter(bardate=bardate).aggregate(Sum('amount'))
        if total_Paytm_amount_Of_The_Month['amount__sum'] == None:
            total_Paytm_amount_Of_The_Month['amount__sum'] = 0
        if total_BharatPe_amount_Of_The_Month['amount__sum'] == None:
            total_BharatPe_amount_Of_The_Month['amount__sum'] = 0
        total_online_amount_Of_The_Month = total_Paytm_amount_Of_The_Month['amount__sum'] + \
                                           total_BharatPe_amount_Of_The_Month['amount__sum']
        if int(month) <= 9:
            month = '0' + str(month)
        expense = Expense.objects.filter(date__contains=str(year) + "-" + str(month)).order_by('date')
        expense_list = []

        amount_returned_to_employees = total_online_amount_Of_The_Month
        print(expense)
        for expenseobj in expense:
            list = []
            list.append(expenseobj.date)
            list.append(expenseobj.purpose)
            list.append(expenseobj.comment)
            list.append(expenseobj.paymentmode)
            list.append(expenseobj.amount)
            amount_returned_to_employees = amount_returned_to_employees + expenseobj.amount
            expense_list.append(list)
        list = []
        list.append('')
        list.append('Remaining Amount')
        list.append('Amount to Employees')
        list.append('Online')
        list.append(amount_returned_to_employees)
        expense_list.append(list)

        month_year_month_name = get_month_year_month_name_for_download()
        return Response({'expense': expense_list,
                        'total_online_amount_Of_The_Month': total_online_amount_Of_The_Month,
                         "month_list": month_year_month_name[0], "year_list": month_year_month_name[2], "month_name": month_year_month_name[1]})


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

def aboutus(request):
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'aboutus.html', {"month_list": month_year_month_name[0], "year_list": month_year_month_name[2], "month_name": month_year_month_name[1]})

@login_required(login_url="/useraccount/login/")
def download(request, download_type, month, year):

    # put the ip address or dns of your apic-em controller in this url
    url=''
    if download_type=='analysis_render' or download_type=='analysis_excel':
        url = 'http://localhost:8000/staff/getAnalysis/'
    elif download_type=='expense':
        url = 'http://localhost:8000/staff/getExpense/'
    payload = {"month": int(month), "year": int(year)}
    print(payload)
    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the response
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)

    # convert response to json format
    r_json = response.json()
    if download_type=='analysis_render':
        pdf = render_to_pdf('analysis.html', r_json)
        return HttpResponse(pdf, content_type='application/pdf')
    elif download_type=='expense':
        pdf = render_to_pdf('expense.html', r_json)
        return HttpResponse(pdf, content_type='application/pdf')
    elif download_type=='analysis_excel':
        print('Excel file is getting ready')
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        # decide file name
        response['Content-Disposition'] = 'attachment; filename='+year+'-'+month+'-analysis.xls'

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
        columns = ['Date', 'Bharatpe', 'Bharatpe Customer', 'Paytm', 'Paytm Customer', 'Cash', 'Cash Customer', 'Total Amount', 'Total Customer']

        # write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        max_length = max(len(r_json['dayWiseBharatpeOfTheMonth']), len(r_json['dayWisePaytmOfTheMonth']), len(r_json['dayWiseCashOfTheMonth']))
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
            ws.write(row_num, 7, int(amount(date, r_json['dayWiseBharatpeOfTheMonth']))+int(amount(date, r_json['dayWisePaytmOfTheMonth']))+int(amount(date, r_json['dayWiseCashOfTheMonth'])), font_style)
            ws.write(row_num, 8, int(numberofcustomer(date, r_json['dayWiseBharatpeOfTheMonth']))+int(numberofcustomer(date, r_json['dayWisePaytmOfTheMonth']))+int(numberofcustomer(date, r_json['dayWiseCashOfTheMonth'])), font_style)

        wb.save(response)
        return response
    # if pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     filename = "Invoice_%s.pdf" % ("12341231")
    #     content = "inline; filename='%s'" % (filename)
    #     download = request.GET.get("download")
    #     if download:
    #         content = "attachment; filename='%s'" % (filename)
    #     response['Content-Disposition'] = content
    #     return response
    # return HttpResponse("Not found")

def shopreg(request):
    if request.method == "POST":
        shopRegistration = ShopRegistration()
        last_shop_id = ShopRegistration.objects.values('ShopID').last()
        new_shop_id = int(str(last_shop_id['ShopID'])[1:]) + 1
        shopRegistration.ShopID = 'O'+str(new_shop_id)
        shopRegistration.Desk_Contact_Number = request.POST.get('Desk_Contact_Number')
        shopRegistration.Shop_Name = request.POST.get('Shop_Name')
        shopRegistration.Shop_Address = request.POST.get('Shop_Address')
        shopRegistration.save()
        messages.success(request, 'Added successfully', extra_tags='alert')
    return render(request, 'shop_registration.html')
