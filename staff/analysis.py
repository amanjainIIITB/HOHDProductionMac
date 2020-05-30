from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from customer.models import BharatPe, Paytm, client
from .views import get_month_year_month_name_for_download
from .common_functions import get_total_online_amount_of_the_month, get_total_cash_amount_of_the_month


def get_last_6_month_data_for_bar_graph(shop_id, year, month):
    now = datetime.datetime.now()
    barGraphNumberOfMonth = 6
    revenueBarGraphData = []
    month_list = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    bharatpe_obj = BharatPe.objects.filter(ShopID=shop_id).values('bardate').annotate(Amount=Sum('amount'),
                                                                                      numberOfCustomer=Sum(
                                                                                          'numberofclient')).order_by(
        '-bardate')
    bharatpe_map = {}
    for obj in bharatpe_obj:
        bharatpe_map[str(obj['bardate'])] = [obj['Amount'], obj['numberOfCustomer']]

    paytm_obj = Paytm.objects.filter(ShopID=shop_id).values('bardate').annotate(Amount=Sum('amount'),
                                                                                numberOfCustomer=Sum(
                                                                                    'numberofclient')).order_by(
        '-bardate')
    paytm_map = {}
    for obj in paytm_obj:
        paytm_map[str(obj['bardate'])] = [obj['Amount'], obj['numberOfCustomer']]

    cash_obj = client.objects.filter(ShopID=shop_id).values('bardate').annotate(Amount=Sum('amount'),
                                                                                numberOfCustomer=Sum(
                                                                                    'numberofclient')).order_by(
        '-bardate')
    cash_map = {}
    for obj in cash_obj:
        cash_map[str(obj['bardate'])] = [obj['Amount'], obj['numberOfCustomer']]

    for index in range(barGraphNumberOfMonth):
        month = month - 1
        if month == -1:
            month = 11
            year = year - 1
        date = str(datetime.datetime(year, month + 1, 1).strftime('%Y-%m-%d'))
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


def get_total_online_customer_of_the_amount(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    number_of_Paytm_customer_Of_The_Month = Paytm.objects.filter(ShopID=shop_id,
                                                                 bardate=bardate).aggregate(Sum('numberofclient'))
    number_of_Bharatpe_customer_Of_The_Month = BharatPe.objects.filter(ShopID=shop_id,
                                                                       bardate=bardate).aggregate(
        Sum('numberofclient'))
    if number_of_Paytm_customer_Of_The_Month['numberofclient__sum'] is None:
        number_of_Paytm_customer_Of_The_Month['numberofclient__sum'] = 0
    if number_of_Bharatpe_customer_Of_The_Month['numberofclient__sum'] == None:
        number_of_Bharatpe_customer_Of_The_Month['numberofclient__sum'] = 0
    number_of_online_customer_Of_The_Month = number_of_Paytm_customer_Of_The_Month['numberofclient__sum'] + \
                                             number_of_Bharatpe_customer_Of_The_Month['numberofclient__sum']
    return number_of_online_customer_Of_The_Month


def get_total_cash_customer_of_the_amount(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    number_of_cash_customer_Of_The_Month = client.objects.filter(ShopID=shop_id,
                                                                 bardate=bardate).aggregate(Sum('numberofclient'))
    if number_of_cash_customer_Of_The_Month['numberofclient__sum'] == None:
        return 0
    else:
        return number_of_cash_customer_Of_The_Month['numberofclient__sum']


def get_day_wise_paytm_of_the_month(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    return Paytm.objects.all().filter(ShopID=shop_id, bardate=bardate).values('date').annotate(
        Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('date')


def get_day_wise_bhratpe_of_the_month(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    return BharatPe.objects.all().filter(ShopID=shop_id, bardate=bardate).values('date').annotate(
        Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('date')


def get_day_wise_cash_of_the_month(shop_id, month, year):
    bardate = datetime.date(day=1, month=month, year=year).strftime('%Y-%m-%d')
    return client.objects.all().filter(ShopID=shop_id, bardate=bardate).values('date').annotate(
        Amount=Sum('amount'), numberOfCustomer=Sum('numberofclient')).order_by('date')


class AnalysisReport(APIView):
    def get(self):
        pass

    def post(self, request):
        month = request.data['month']
        year = request.data['year']
        month_year_month_name = get_month_year_month_name_for_download()
        return Response(
            {'revenueBarGraphData': get_last_6_month_data_for_bar_graph(request.data['shop_id'], year, month),
             'dayWiseBharatpeOfTheMonth': get_day_wise_bhratpe_of_the_month(request.data['shop_id'], month, year),
             'dayWisePaytmOfTheMonth': get_day_wise_paytm_of_the_month(request.data['shop_id'], month, year),
             'dayWiseCashOfTheMonth': get_day_wise_cash_of_the_month(request.data['shop_id'], month, year),
             'listOfDates': prepare_list_of_dates(year, month),
             'total_cash_amount_Of_The_Month': get_total_cash_amount_of_the_month(request.data['shop_id'], month, year),
             'total_online_amount_Of_The_Month': get_total_online_amount_of_the_month(request.data['shop_id'], month,
                                                                                      year),
             'number_of_cash_customer_Of_The_Month': get_total_cash_customer_of_the_amount(request.data['shop_id'],
                                                                                           month, year),
             'number_of_online_customer_Of_The_Month': get_total_online_customer_of_the_amount(request.data['shop_id'],
                                                                                               month, year),
             'month_list': month_year_month_name[0],
             'year_list': month_year_month_name[2],
             'month_name': month_year_month_name[1]})
