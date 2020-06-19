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
    return render(request, 'details.html', {"month_list": month_year_month_name[0], 
                                            "year_list": month_year_month_name[2], 
                                            "month_name": month_year_month_name[1], 
                                            "shop_details": get_login_user_shop_details(request),
                                            "shop_id": request.session['shop_id']})


def save_customer_membership(request):
    membership = Membership()
    membership.custID = request.POST.get('custid')
    membership.shopID = request.session['shop_id']
    membership.Name = request.POST.get('name')
    membership.Sex = request.POST.get('sex')
    membership.Contact_Number = request.POST.get('contact_number')
    membership.DOB = request.POST.get('date')
    membership.save()
    messages.success(request, 'Added successfully', extra_tags='alert')


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
                                                "shop_id": request.session['shop_id']})
