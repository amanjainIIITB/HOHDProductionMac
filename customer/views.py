from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from staff.models import Employee
from HOHDProductionMac.common_function import get_month_year_month_name_for_download, atleast_one_shop_registered, \
    get_login_user_shop_details, get_current_time
import datetime
# Create your views here.


def update_non_mem_client_visit(request, visit_id):
    if request.method == "POST":
        ClientVisit.objects.filter(visitID=visit_id, ShopID=request.session['shop_id']).update(date=request.POST.get('date'), time=get_current_time(),
                       numberofclient=request.POST.get('numberofclient'), employee_id=request.POST.get('employee'), payment_mode=request.POST.get('payment_mode'), amount=request.POST.get('amount'))
        # messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/analysis/')
    else:
        client_data = ClientVisit.objects.values('visitID', 'date', 'employee_id', 'payment_mode', 'numberofclient', 'amount').filter(visitID=visit_id, ShopID=request.session['shop_id']).last()
    return render(request, 'update_non_mem_client_visit.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                                'client_data': client_data, 
                                                                "employees": Employee.objects.values('EmployeeID', 'name').filter(ShopID=request.session['shop_id']),
                                                                "shop_details": get_login_user_shop_details(request)})


def update_membership_after_update_mem_client_visit(request, custID):
    client_visit = ClientVisit.objects.values('date').filter(custID=custID, ShopID=request.session['shop_id']).order_by('date').last()
    Membership.objects.filter(custID=custID, shopID=request.session['shop_id']).update(last_visit=client_visit['date'])


def update_mem_client_visit(request, visit_id):
    if request.method == "POST":
        ClientVisit.objects.filter(visitID=visit_id, ShopID=request.session['shop_id']).update(custID=request.POST.get('custID'), date=request.POST.get('date'),
                       time=get_current_time(), employee_id=request.POST.get('EmployeeID'), payment_mode=request.POST.get('payment_mode'), amount=request.POST.get('amount'))
        update_membership_after_update_mem_client_visit(request, request.POST.get('custID'))
        # messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/staff/analysis/')
    else:
        client_data = ClientVisit.objects.values('visitID', 'custID', 'date', 'employee_id', 'payment_mode', 'amount').filter(visitID=visit_id, ShopID=request.session['shop_id']).last()
    return render(request, 'update_mem_client_visit.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                            'client_data': client_data,
                                                            "employees": Employee.objects.values('EmployeeID', 'name').filter(ShopID=request.session['shop_id']),
                                                            "membership_based_on_shop_id": list(get_all_membership_based_on_shop_id(request)),
                                                            "shop_details": get_login_user_shop_details(request)})


def delete_client_visit(request, visit_id):
    ClientVisit.objects.filter(visitID=visit_id, ShopID=request.session['shop_id']).delete()
    return redirect('/staff/analysis/')


def get_new_visit_id(request):
    last_visit_id = ClientVisit.objects.values('visitID').filter(ShopID=request.session['shop_id']).last()
    if last_visit_id == None:
        return 'V0'
    else:
        new_visit_id = 'V' + str(int(str(last_visit_id['visitID'])[1:]) + 1)
        return new_visit_id


@login_required(login_url="/")
def details(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if request.method == "POST":
        now = datetime.datetime.now()
        custID=request.POST.get('client_id')
        if custID=='':
            paymentmode = request.POST.get('paymentmode')
            datesplit = request.POST.get('date').split('-')
            y = int(datesplit[0])
            m = int(datesplit[1])
            if (paymentmode == 'cash'):
                print('cash payment for non-membership customer')
                ClientVisit(isMember=False, custID='None' ,visitID=get_new_visit_id(request), date=request.POST.get('date'), payment_mode='cash', employee_id=request.POST.get('EmployeeID'), ShopID=request.session['shop_id'], bardate=datetime.date(day=1, month=m, year=y).strftime("%Y-%m-%d"), time=get_current_time(), numberofclient=request.POST.get('numberofclient'), amount=request.POST.get('amount')).save()
            else:
                print('online payment for non-membership customer')
                ClientVisit(isMember=False, custID='None' ,visitID=get_new_visit_id(request), date=request.POST.get('date'), payment_mode='online', employee_id=request.POST.get('EmployeeID'), ShopID=request.session['shop_id'], bardate=datetime.date(day=1, month=m, year=y).strftime("%Y-%m-%d"), time=get_current_time(), numberofclient=request.POST.get('numberofclient'), amount=request.POST.get('amount')).save()
            messages.success(request, 'Added successfully', extra_tags='alert')
        else:
            paymentmode = request.POST.get('mem_paymentmode')
            datesplit = request.POST.get('mem_date').split('-')
            custID = custID.upper()
            y = int(datesplit[0])
            m = int(datesplit[1])
            update_membership_after_service(request, custID, request.POST.get('mem_amount'), request.POST.get('mem_date'))
            if (paymentmode == 'cash'):
                print('cash payment for membership customer')
                ClientVisit(isMember=True, custID=custID ,visitID=get_new_visit_id(request), date=request.POST.get('mem_date'), payment_mode='cash', employee_id=request.POST.get('mem_EmployeeID'), ShopID=request.session['shop_id'], bardate=datetime.date(day=1, month=m, year=y).strftime("%Y-%m-%d"), time=get_current_time(), numberofclient=1, amount=request.POST.get('mem_amount')).save()
            else:
                print('online payment for membership customer')
                ClientVisit(isMember=True, custID=custID ,visitID=get_new_visit_id(request), date=request.POST.get('mem_date'), payment_mode='online', employee_id=request.POST.get('mem_EmployeeID'), ShopID=request.session['shop_id'], bardate=datetime.date(day=1, month=m, year=y).strftime("%Y-%m-%d"), time=get_current_time(), numberofclient=1, amount=request.POST.get('mem_amount')).save()
            messages.success(request, 'Added successfully', extra_tags='alert')
    employees = Employee.objects.values('EmployeeID', 'name').filter(ShopID=request.session['shop_id'])
    return render(request, 'details.html', {"month_year_month_name": get_month_year_month_name_for_download(), 
                                            "shop_details": get_login_user_shop_details(request),
                                            "membership_based_on_shop_id": list(get_all_membership_based_on_shop_id(request)),
                                            "employees": employees})


def get_all_membership():
    memberships = Membership.objects.all()
    list_users = []
    for membership in memberships:
        user = [membership.custID, membership.Contact_Number, membership.Sex,
                membership.Name, membership.shopID]
        list_users.append(user)
    return list_users


def get_all_membership_based_on_shop_id(request):
    memberships = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit', 'total_amount', 'number_of_visit').filter(shopID=request.session['shop_id'])
    for membership in memberships:
        membership['DOB'] = membership['DOB'].strftime("%Y-%m-%d")
        membership['last_visit'] = membership['last_visit'].strftime("%Y-%m-%d")
        if membership['total_amount'] == 0 or membership['number_of_visit'] == 0:
            membership['avg'] = 0
        else:
            membership['avg'] = round(membership['total_amount']/membership['number_of_visit'], 2)
    return memberships


@login_required(login_url="/")
def membership(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if request.method == "POST":
        Membership(custID=request.POST.get('custid').upper(), shopID=request.session['shop_id'], Name=request.POST.get('name'), Sex=request.POST.get('sex'), Contact_Number=request.POST.get('contact_number'), DOB=request.POST.get('DOB')).save()
        messages.success(request, 'Added successfully', extra_tags='alert')
    return render(request, 'membership.html', {"month_year_month_name": get_month_year_month_name_for_download(), 
                                                "shop_details": get_login_user_shop_details(request),
                                                "memberships": list(get_all_membership_based_on_shop_id(request))})


def update_client_visit_after_update_membership(current_client_id, changed_client_id, shop_id):
    ClientVisit.objects.filter(custID=current_client_id, ShopID=shop_id).update(custID=changed_client_id)


def update_membership(request, cust_id):
    if request.method == "POST":
        membership = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB'). \
            filter(shopID=request.session['shop_id'], custID=cust_id)
        membership.update(custID=request.POST.get('custID').upper(), Contact_Number=request.POST.get('Contact_Number'),
                       Sex=request.POST.get('Sex'), Name=request.POST.get('Name'),
                       DOB=request.POST.get('DOB'))
        update_client_visit_after_update_membership(cust_id, request.POST.get('custID').upper(), request.session['shop_id'])
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/client/membership')
    else:
        membership = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB'). \
            filter(shopID=request.session['shop_id'], custID=cust_id).last()
        return render(request, 'update_membership.html', { "month_year_month_name": get_month_year_month_name_for_download(),
                                                           'custID': membership['custID'],
                                                           'Contact_Number': membership['Contact_Number'],
                                                           'Sex': membership['Sex'],
                                                           'Name': membership['Name'],
                                                           'DOB': membership['DOB'],
                                                           'memberships': list(get_all_membership_based_on_shop_id(request)),
                                                           "shop_details": get_login_user_shop_details(request)})

def delete_all_visit_of_client(client_id, shop_id):
    ClientVisit.objects.filter(custID=client_id, ShopID=shop_id).update(isMember=False, custID='None')


def delete_membership(request, cust_id):
    Membership.objects.filter(custID=cust_id, shopID=request.session['shop_id']).delete()
    delete_all_visit_of_client(cust_id, request.session['shop_id'])
    return redirect('/client/membership/')


def update_membership_after_service(request, cust_id, amount, date):
    membership = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit', 'total_amount', 'number_of_visit').filter(shopID=request.session['shop_id'], custID=cust_id)
    membership.update(last_visit=date, total_amount=membership[0]['total_amount']+int(amount), number_of_visit=membership[0]['number_of_visit']+1)