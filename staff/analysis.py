from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from staff.models import Employee
from customer.models import ClientVisit
from .views import get_month_year_month_name_for_download
from .common_functions import get_total_online_amount_of_the_month, get_total_cash_amount_of_the_month, get_bardate
from HOHDProductionMac.common_function import convert_date_dd_mm_yyyy_to_yyyy_mm_dd, convert_date_yyyy_mm_dd_to_dd_mm_yyyy

def get_last_6_month_data_for_bar_graph(shop_id, year, month):
    now = datetime.datetime.now()
    barGraphNumberOfMonth = 6
    revenueBarGraphData = []
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    for index in range(barGraphNumberOfMonth):
        if month == 0:
            month = 12
            year = year - 1
        online = ClientVisit.objects.filter(payment_mode='online', ShopID=shop_id, date__contains=get_bardate(month, year)).aggregate(Amount=Sum('amount'),
                                                                                      numberOfCustomer=Sum('numberofclient'))
        cash = ClientVisit.objects.filter(payment_mode='cash', ShopID=shop_id, date__contains=get_bardate(month, year)).aggregate(Amount=Sum('amount'),
                                                                                      numberOfCustomer=Sum('numberofclient'))
        online_amount = 0
        cash_amount = 0
        online_numberofcustomer = 0
        cash_numberofcustomer = 0
        if online['Amount'] is not None:
            online_amount = online['Amount']
        if cash['Amount'] is not None:
            cash_amount = cash['Amount']
        if online['numberOfCustomer'] is not None:
            online_numberofcustomer = online['numberOfCustomer']
        if cash['numberOfCustomer'] is not None:
            cash_numberofcustomer = cash['numberOfCustomer']
        month = month - 1
        revenueBarGraphData.append([month_list[month], online_amount+cash_amount, online_numberofcustomer+cash_numberofcustomer, online_amount, cash_amount, online_numberofcustomer, cash_numberofcustomer])
    return revenueBarGraphData[::-1]


def prepare_list_of_dates(year, month):
    now = datetime.datetime.now()
    number_of_days = 0
    if month == now.month:
        number_of_days = datetime.datetime.today().day
    else:
        if month == 12:
            number_of_days = (datetime.datetime(year + 1, 1, 1) - datetime.datetime(year, month, 1)).days
        else:
            number_of_days = (datetime.datetime(year, month + 1, 1) - datetime.datetime(year, month, 1)).days
    listOfDates = []
    day = 1
    while day <= number_of_days:
        listOfDates.append(datetime.date(day=day, month=month, year=year).strftime('%Y-%m-%d'))
        day = day + 1
    return listOfDates


def get_total_online_customer_of_the_month(shop_id, month, year):
    number_of_online_customer_Of_The_Month = ClientVisit.objects.filter(payment_mode='online', ShopID=shop_id,
                                                                 date__contains=get_bardate(month, year)).aggregate(Sum('numberofclient'))
    if number_of_online_customer_Of_The_Month['numberofclient__sum'] is None:
        return 0
    return number_of_online_customer_Of_The_Month['numberofclient__sum']


def get_total_cash_customer_of_the_month(shop_id, month, year):
    number_of_cash_customer_Of_The_Month = ClientVisit.objects.filter(payment_mode='cash', ShopID=shop_id,
                                                                 date__contains=get_bardate(month, year)).aggregate(Sum('numberofclient'))
    if number_of_cash_customer_Of_The_Month['numberofclient__sum'] == None:
        return 0
    else:
        return number_of_cash_customer_Of_The_Month['numberofclient__sum']


def get_day_wise_online_of_the_month(shop_id, month, year):
    return ClientVisit.objects.all().filter(payment_mode='online', ShopID=shop_id, date__contains=get_bardate(month, year)).values('date').annotate(
        Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('date')


def get_day_wise_cash_of_the_month(shop_id, month, year):
    return ClientVisit.objects.all().filter(payment_mode='cash', ShopID=shop_id, date__contains=get_bardate(month, year)).values('date').annotate(
        Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('date')


def get_all_client_data_of_the_month(shop_id):
    client_visit_objects =  ClientVisit.objects.values('custID', 'isMember', 'visitID', 'date', 'payment_mode', 'time', 'employee_id', 'amount', 'numberofclient').filter(ShopID=shop_id).order_by('date')
    for client_visit_object in client_visit_objects:
        # client_visit_object['date'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(str(client_visit_object['date']))
        emp_queryset = Employee.objects.values('name').filter(ShopID=shop_id, EmployeeID=client_visit_object['employee_id'])
        if len(emp_queryset) != 0:
            client_visit_object['employee'] = emp_queryset.first()['name']
    return client_visit_objects


class AnalysisReport(APIView):
    def get(self):
        pass

    def post(self, request):
        month = request.data['month']
        year = request.data['year']
        return Response(
            {'revenueBarGraphData': get_last_6_month_data_for_bar_graph(request.data['shop_id'], year, month),
             'dayWiseOnlineOfTheMonth': get_day_wise_online_of_the_month(request.data['shop_id'], month, year),
             'dayWiseCashOfTheMonth': get_day_wise_cash_of_the_month(request.data['shop_id'], month, year),
             'listOfDates': prepare_list_of_dates(year, month),
             'client_data_based_on_shop_id': get_all_client_data_of_the_month(request.data['shop_id']),
             'total_cash_amount_Of_The_Month': get_total_cash_amount_of_the_month(request.data['shop_id'], month, year),
             'total_online_amount_Of_The_Month': get_total_online_amount_of_the_month(request.data['shop_id'], month, year),
             'number_of_cash_customer_Of_The_Month': get_total_cash_customer_of_the_month(request.data['shop_id'], month, year),
             'number_of_online_customer_Of_The_Month': get_total_online_customer_of_the_month(request.data['shop_id'], month, year),
             "month_year_month_name": get_month_year_month_name_for_download()})
