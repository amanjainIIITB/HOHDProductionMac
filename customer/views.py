from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from staff.models import Employee, ShopRegistration
from staff.views import analysis
from customer.models import Services
from HOHDProductionMac.common_function import atleast_one_shop_registered, get_current_time, get_all_membership_based_on_shop_id, convert_date_yyyy_mm_dd_to_dd_mm_yyyy, get_services, is_page_accessible, get_all_services, get_common_attributes
import datetime
from staff.common_functions import get_bardate
# Create your views here.


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
            print('Service ids', service_ids)
            for service_id in service_ids:
                if service_id != '' and service_id in all_services_dict:
                    service_names.append(all_services_dict[service_id])
            client_visit_object['services'] = ",".join(service_names)
    return client_visit_objects

    
def save_client_services(request, visitID):
    service_ids = request.POST.getlist('services[]')
    client_service_ids = ''
    for service_id in service_ids:
        Services(visitID=visitID, date=request.POST.get('date'), ServiceID=service_id, shopID=request.session['shop_id']).save()
        client_service_ids = ",".join(request.POST.getlist('services[]'))
    return client_service_ids


def update_client_services(request, visitID):
    services = Services.objects.filter(visitID=visitID, shopID=request.session['shop_id'])
    if services is not None:
        services.delete()
    service_ids = request.POST.getlist('services[]')
    client_service_ids = ''
    for service_id in service_ids:
        Services(visitID=visitID, date=request.POST.get('date'), ServiceID=service_id, shopID=request.session['shop_id']).save()
        client_service_ids = ",".join(request.POST.getlist('services[]'))
    return client_service_ids


def update_non_mem_client_visit(request, visit_id):
    if request.method == "POST":
        if is_page_accessible(request, "update_non_mem_client_visit") == False:
            return redirect('/staff/aboutus/') 
        ClientVisit.objects.filter(visitID=visit_id, ShopID=request.session['shop_id']).update(date=request.POST.get('date'), services=update_client_services(request, visit_id), time=get_current_time(),
                       numberofclient=request.POST.get('numberofclient'), employee_id=request.POST.get('employee'), payment_mode=request.POST.get('payment_mode'), amount=request.POST.get('amount'))
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/analysis/')
    else:
        client_data = ClientVisit.objects.values('visitID', 'date', 'services', 'employee_id', 'payment_mode', 'numberofclient', 'amount').filter(visitID=visit_id, ShopID=request.session['shop_id']).last()
    served_services = set()
    if client_data['services'] is not None:
        served_services = set(client_data['services'].split(","))
    attributes_json = {
        'client_data': client_data, 
        "served_services": served_services,
        "services": get_services(),
        "employees": Employee.objects.values('EmployeeID', 'name').filter(ShopID=request.session['shop_id'])
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'update_non_mem_client_visit.html', attributes_json)



def update_mem_client_visit(request, visit_id):
    if request.method == "POST":
        if is_page_accessible(request, "update_mem_client_visit") == False:
            return redirect('/staff/aboutus/') 
        ClientVisit.objects.filter(visitID=visit_id, ShopID=request.session['shop_id']).update(custID=request.POST.get('custID'), services=update_client_services(request, visit_id), date=request.POST.get('date'),
                       time=get_current_time(), employee_id=request.POST.get('EmployeeID'), payment_mode=request.POST.get('payment_mode'), amount=request.POST.get('amount'))
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/analysis/')
    else:
        client_data = ClientVisit.objects.values('visitID', 'custID', 'services', 'date', 'employee_id', 'payment_mode', 'amount').filter(visitID=visit_id, ShopID=request.session['shop_id']).last()
    served_services = set()
    if client_data['services'] is not None:
        served_services = set(client_data['services'].split(","))
    attributes_json = {
        'client_data': client_data,
        "employees": Employee.objects.values('EmployeeID', 'name').filter(ShopID=request.session['shop_id']),
        "memberships": list(get_all_membership_based_on_shop_id(request, request.session['shop_id'])),
        "served_services": served_services,
        "services": get_services()
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'update_mem_client_visit.html', attributes_json)



def delete_client_visit(request, visit_id):
    if is_page_accessible(request, "delete_client_visit") == False:
        return redirect('/staff/aboutus/') 
    ClientVisit.objects.filter(visitID=visit_id, ShopID=request.session['shop_id']).delete()
    Services.objects.filter(visitID=visit_id, shopID=request.session['shop_id']).delete()
    messages.success(request, 'Deleted successfully', extra_tags='alert')
    return redirect('/staff/analysis/')


def get_new_visit_id(request):
    last_visit_id = ClientVisit.objects.values('visitID').filter(ShopID=request.session['shop_id']).last()
    if last_visit_id == None:
        return 'V0'
    else:
        new_visit_id = 'V' + str(int(str(last_visit_id['visitID'])[1:]) + 1)
        return new_visit_id


@login_required(login_url="/")
def save_mem_visit(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    else:
        if is_page_accessible(request, "save_mem_visit") == False:
            return redirect('/staff/aboutus/') 
        visitID=get_new_visit_id(request)
        membership = Membership.objects.values('custID').filter(shopID=request.session['shop_id'], Contact_Number=request.POST.get('Contact_Number')).first()
        paymentmode = request.POST.get('mem_paymentmode')
        if (paymentmode == 'cash'):
            print('cash payment for membership customer')
            ClientVisit(isMember=True, custID=membership['custID'] ,visitID=visitID, services=save_client_services(request, visitID), date=request.POST.get('date'), payment_mode='cash', employee_id=request.POST.get('mem_EmployeeID'), ShopID=request.session['shop_id'], time=get_current_time(), numberofclient=1, amount=request.POST.get('mem_amount')).save()
        else:
            print('online payment for membership customer')
            ClientVisit(isMember=True, custID=membership['custID'] ,visitID=visitID, services=save_client_services(request, visitID), date=request.POST.get('date'), payment_mode='online', employee_id=request.POST.get('mem_EmployeeID'), ShopID=request.session['shop_id'], time=get_current_time(), numberofclient=1, amount=request.POST.get('mem_amount')).save()
        messages.success(request, 'Added successfully', extra_tags='alert')
    return redirect('/client/details/')


@login_required(login_url="/")
def save_non_mem_visit(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    else:
        if is_page_accessible(request, "save_non_mem_visit") == False:
            return redirect('/staff/aboutus/') 
        paymentmode = request.POST.get('paymentmode')
        visitID=get_new_visit_id(request)
        if (paymentmode == 'cash'):
            print('cash payment for non-membership customer')
            ClientVisit(isMember=False, custID='None' ,visitID=visitID, services=save_client_services(request, visitID), date=request.POST.get('date'), payment_mode='cash', employee_id=request.POST.get('EmployeeID'), ShopID=request.session['shop_id'], time=get_current_time(), numberofclient=request.POST.get('numberofclient'), amount=request.POST.get('amount')).save()
        else:
            print('online payment for non-membership customer')
            ClientVisit(isMember=False, custID='None' ,visitID=visitID, services=save_client_services(request, visitID), date=request.POST.get('date'), payment_mode='online', employee_id=request.POST.get('EmployeeID'), ShopID=request.session['shop_id'], time=get_current_time(), numberofclient=request.POST.get('numberofclient'), amount=request.POST.get('amount')).save()
        messages.success(request, 'Added successfully', extra_tags='alert')
    return redirect('/client/details/')



@login_required(login_url="/")
def details(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "details") == False:
        return redirect('/staff/aboutus/') 
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    employees = Employee.objects.values('EmployeeID', 'name').filter(ShopID=request.session['shop_id'])
    attributes_json = {"memberships": list(get_all_membership_based_on_shop_id(request, request.session['shop_id'])),
        "employees": employees,
        'client_data_based_on_shop_id': get_all_client_data_of_the_month(request.session['shop_id'], month, year),
        "served_services": set(),
        "services": get_services()
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'details.html', attributes_json)


def get_all_membership():
    memberships = Membership.objects.all()
    list_users = []
    for membership in memberships:
        user = [membership.custID, membership.Contact_Number, membership.Sex,
                membership.Name, membership.shopID]
        list_users.append(user)
    return list_users


@login_required(login_url="/")
def create_membership(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "create_membership") == False:
        return redirect('/staff/aboutus/') 
    Membership(custID=request.POST.get('custid').upper(), shopID=request.session['shop_id'], Name=request.POST.get('name'), Sex=request.POST.get('sex'), Contact_Number=request.POST.get('contact_number'), DOB=request.POST.get('DOB')).save()
    messages.success(request, 'Added successfully', extra_tags='alert')
    return redirect('/client/membership/')


@login_required(login_url="/")
def membership(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if is_page_accessible(request, "membership") == False:
        return redirect('/staff/aboutus/') 
    attributes_json = {
        "memberships": list(get_all_membership_based_on_shop_id(request, request.session['shop_id']))
    }
    get_common_attributes(request, attributes_json)
    return render(request, 'membership.html', attributes_json)


def update_client_visit_after_update_membership(current_client_id, changed_client_id, shop_id):
    ClientVisit.objects.filter(custID=current_client_id, ShopID=shop_id).update(custID=changed_client_id)


def update_membership(request, cust_id):
    if request.method == "POST":
        if is_page_accessible(request, "update_membership") == False:
            return redirect('/staff/aboutus/') 
        membership = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB'). \
            filter(shopID=request.session['shop_id'], custID=cust_id)
        membership.update(custID=request.POST.get('custID').upper(), Contact_Number=request.POST.get('Contact_Number'),
                    Sex=request.POST.get('Sex'), Name=request.POST.get('Name'), DOB=request.POST.get('DOB'))
        update_client_visit_after_update_membership(cust_id, request.POST.get('custID').upper(), request.session['shop_id'])
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/client/membership')
    else:
        membership = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB'). \
            filter(shopID=request.session['shop_id'], custID=cust_id).last()
        attributes_json = { 'custID': membership['custID'],
            'Contact_Number': membership['Contact_Number'],
            'Sex': membership['Sex'],
            'Name': membership['Name'],
            'DOB': membership['DOB'],
            'memberships': list(get_all_membership_based_on_shop_id(request, request.session['shop_id']))
        }
        get_common_attributes(request, attributes_json)
        return render(request, 'update_membership.html', attributes_json)

def delete_all_visit_of_client(client_id, shop_id):
    ClientVisit.objects.filter(custID=client_id, ShopID=shop_id).update(isMember=False, custID='None')


def delete_membership(request, cust_id):
    if is_page_accessible(request, "delete_membership") == False:
        return redirect('/staff/aboutus/') 
    Membership.objects.filter(custID=cust_id, shopID=request.session['shop_id']).delete()
    delete_all_visit_of_client(cust_id, request.session['shop_id'])
    messages.success(request, 'Deleted successfully', extra_tags='alert')
    return redirect('/client/membership/')

