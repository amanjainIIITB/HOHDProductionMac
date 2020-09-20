from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from staff.models import Employee
from customer.models import ClientVisit, Services
from .views import get_month_year_month_name_for_download
from .common_functions import get_total_online_amount_of_the_month, get_total_cash_amount_of_the_month, get_bardate
from HOHDProductionMac.common_function import convert_date_dd_mm_yyyy_to_yyyy_mm_dd, convert_date_yyyy_mm_dd_to_dd_mm_yyyy, get_services, get_all_services

def get_services_of_the_month(shop_id, year, month):

    all_services_dict = get_all_services()

    # set month and year, if they are out of range
    if month==0:
        year = year-1
        month=12

    services_list = get_services()
    served_services = {}

    #create dictionary for the served services
    services = Services.objects.values('ServiceID').filter(shopID=shop_id, date__contains=get_bardate(month, year)).annotate(service_count=Count('ServiceID'))
    for service_obj in services:
        served_services[service_obj['ServiceID']] = service_obj['service_count']

    # Check Hair Services
    hair_services = {}
    for hair_service_id in services_list['hair']:
        if hair_service_id in served_services.keys():
            hair_services[all_services_dict[hair_service_id]] = served_services[hair_service_id]
        else:
            hair_services[all_services_dict[hair_service_id]] = 0

    # Check Face Services
    face_services = {}
    for face_service_id in services_list['face']:
        if face_service_id in served_services.keys():
            face_services[all_services_dict[face_service_id]] = served_services[face_service_id]
        else:
            face_services[all_services_dict[face_service_id]] = 0

    # Check other Services
    other_services = {}
    for other_service_id in services_list['other']:
        if other_service_id in served_services.keys():
            other_services[all_services_dict[other_service_id]] = served_services[other_service_id]
        else:
            other_services[all_services_dict[other_service_id]] = 0

    print({ 'hair': hair_services, 'face': face_services, 'other': other_services })
    return { 'hair': hair_services, 'face': face_services, 'other': other_services }


def get_staff_contribution(shop_id, year, month):
    emp_ids = Employee.objects.values('EmployeeID', 'name').filter(ShopID=shop_id)
    staff_contribution_list = []
    print('Data')
    print(ClientVisit.objects.values('employee_id').filter(ShopID=shop_id, date__contains=get_bardate(month, year)).annotate(Amount=Sum('amount'),
                                                                                      numberOfCustomer=Sum('numberofclient')))
    for emp_id in emp_ids:
        staff_contibution_structure = {}
        staff_contibution_structure['name'] = emp_id['name']
        online = ClientVisit.objects.filter(payment_mode='online', ShopID=shop_id, employee_id=emp_id['EmployeeID'], date__contains=get_bardate(month, year)).aggregate(Amount=Sum('amount'),
                                                                                      numberOfCustomer=Sum('numberofclient'))
        cash = ClientVisit.objects.filter(payment_mode='cash', ShopID=shop_id, employee_id=emp_id['EmployeeID'], date__contains=get_bardate(month, year)).aggregate(Amount=Sum('amount'),
                                                                                      numberOfCustomer=Sum('numberofclient'))
        if online['Amount'] is None:
            online['Amount'] = 0
        if cash['Amount'] is None:
            cash['Amount'] = 0
        if online['numberOfCustomer'] is None:
            online['numberOfCustomer'] = 0
        if cash['numberOfCustomer'] is None:
            cash['numberOfCustomer'] = 0
        staff_contibution_structure['total_amount'] = online['Amount'] + cash['Amount']
        staff_contibution_structure['total_customer'] = online['numberOfCustomer'] + cash['numberOfCustomer']
        staff_contibution_structure['online_amount'] = online['Amount']
        staff_contibution_structure['online_numberofcustomer'] = online['numberOfCustomer']
        staff_contibution_structure['cash_amount'] = cash['Amount']
        staff_contibution_structure['cash_numberofcustomer'] = cash['numberOfCustomer']
        staff_contribution_list.append(staff_contibution_structure)
    return staff_contribution_list



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


def get_all_client_data_of_the_month(shop_id, month, year):
    all_services_dict = get_all_services()
    client_visit_objects =  ClientVisit.objects.values('custID', 'isMember', 'services', 'visitID', 'date', 'payment_mode', 'time', 'employee_id', 'amount', 'numberofclient').filter(ShopID=shop_id, date__contains=get_bardate(month, year)).order_by('date')
    for client_visit_object in client_visit_objects:
        # client_visit_object['date'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(str(client_visit_object['date']))
        emp_queryset = Employee.objects.values('name').filter(ShopID=shop_id, EmployeeID=client_visit_object['employee_id'])
        if len(emp_queryset) != 0:
            client_visit_object['employee'] = emp_queryset.first()['name']
        if client_visit_object['services'] is not None:
            service_ids = client_visit_object['services'].split(",")
            service_names = []
            client_visit_object['services'] = ''
            for service_id in service_ids:
                service_names.append(all_services_dict[service_id])
            client_visit_object['services'] = ",".join(service_names)
    return client_visit_objects


class AnalysisReport(APIView):
    def get(self):
        pass

    def post(self, request):
        month = request.data['month']
        print('month is')
        print(month)
        year = request.data['year']
        return Response(
            {'services_of_the_month': get_services_of_the_month(request.data['shop_id'], year, month),
             'services_of_the_previous_month': get_services_of_the_month(request.data['shop_id'], year, month-1),
             'staff_contribution': get_staff_contribution(request.data['shop_id'], year, month),
             'revenueBarGraphData': get_last_6_month_data_for_bar_graph(request.data['shop_id'], year, month),
             'dayWiseOnlineOfTheMonth': get_day_wise_online_of_the_month(request.data['shop_id'], month, year),
             'dayWiseCashOfTheMonth': get_day_wise_cash_of_the_month(request.data['shop_id'], month, year),
             'listOfDates': prepare_list_of_dates(year, month),
             'client_data_based_on_shop_id': get_all_client_data_of_the_month(request.data['shop_id'], month, year),
             'total_cash_amount_Of_The_Month': get_total_cash_amount_of_the_month(request.data['shop_id'], month, year),
             'total_online_amount_Of_The_Month': get_total_online_amount_of_the_month(request.data['shop_id'], month, year),
             'number_of_cash_customer_Of_The_Month': get_total_cash_customer_of_the_month(request.data['shop_id'], month, year),
             'number_of_online_customer_Of_The_Month': get_total_online_customer_of_the_month(request.data['shop_id'], month, year),
             "month_year_month_name": get_month_year_month_name_for_download()})
