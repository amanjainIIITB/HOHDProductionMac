from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from HOHDProductionMac.common_function import get_month_year_month_name_for_download, atleast_one_shop_registered, \
    get_login_user_shop_details
# Create your views here.


def select_payment_mode_object(paymentmode):
    customer = ''
    if (paymentmode == 'Bharatpe'):
        customer = BharatPe()
    elif (paymentmode == 'Paytm'):
        customer = Paytm()
    elif (paymentmode == 'Cash'):
        customer = client()
    return customer


def save_customer_entry(request, customer, date, bardate, time, paymentmode, amount, numberofclient):
    customer.date = date
    customer.ShopID = request.session['shop_id']
    customer.bardate = bardate
    customer.time = time
    customer.paymentmode = paymentmode
    customer.amount = amount
    customer.numberofclient = numberofclient
    customer.save()
    messages.success(request, 'Added successfully', extra_tags='alert')


@login_required(login_url="/useraccount/login/")
def details(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if request.method == "POST":
        paymentmode = request.POST.get('paymentmode')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        numberofclient = request.POST.get('numberofclient')
        now = datetime.datetime.now()
        datesplit = date.split('-')
        Y = int(datesplit[0])
        m = int(datesplit[1])
        bardate = datetime.datetime(Y, m, 1)
        time = now.strftime('%H:%M:%S')
        customer = select_payment_mode_object(paymentmode)
        save_customer_entry(request, customer, date, bardate, time, paymentmode, amount, numberofclient)
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'details.html', {"month_list": month_year_month_name[0], "year_list": month_year_month_name[2], "month_name": month_year_month_name[1], "shop_details": get_login_user_shop_details(request)})


def save_customer_membership(request):
    membership = Membership()
    membership.custID = request.POST.get('custid')
    membership.shopID = request.session['shop_id']
    membership.Name = request.POST.get('name')
    membership.Sex = request.POST.get('sex')
    membership.Contact_Number = request.POST.get('contact_number')
    membership.DOB = request.POST.get('DOB')
    membership.save()
    messages.success(request, 'Added successfully', extra_tags='alert')


def get_all_membership(request):
    memberships = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit', 'total_amount', 'number_of_visit').filter(shopID=request.session['shop_id'])
    for membership in memberships:
        if membership['total_amount'] == 0 or membership['number_of_visit'] == 0:
            membership['avg'] = 0
        else:
            membership['avg'] = round(membership['total_amount']/membership['number_of_visit'], 2)
    print('Inside Membership')
    print(memberships)
    return memberships

@login_required(login_url="/useraccount/login/")
def membership(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if request.method == "POST":
        save_customer_membership(request)
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'membership.html', {"month_list": month_year_month_name[0], 
                                                "year_list": month_year_month_name[2], 
                                                "month_name": month_year_month_name[1], 
                                                "shop_details": get_login_user_shop_details(request),
                                                "memberships": get_all_membership(request)})



def update_membership(request, cust_id):
    if request.method == "POST":
        membership = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB'). \
            filter(shopID=request.session['shop_id'], custID=cust_id)
        membership.update(custID=request.POST.get('custID'), Contact_Number=request.POST.get('Contact_Number'),
                       Sex=request.POST.get('Sex'), Name=request.POST.get('Name'),
                       DOB=request.POST.get('DOB'))
        messages.success(request, 'Updated successfully', extra_tags='alert')
        return redirect('/client/membership')
    else:
        membership = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB'). \
            filter(shopID=request.session['shop_id'], custID=cust_id).last()
        print(membership)
        return render(request, 'update_membership.html', {'custID': membership['custID'],
                                                           'Contact_Number': membership['Contact_Number'],
                                                           'Sex': membership['Sex'],
                                                           'Name': membership['Name'],
                                                           'DOB': membership['DOB']})