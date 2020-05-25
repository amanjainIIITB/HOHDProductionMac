from django.shortcuts import render, redirect
from .models import *
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from staff.views import atleast_one_shop_registered, get_month_year_month_name_for_download, get_shop_details
# Create your views here.


@login_required(login_url="/useraccount/login/")
def details(request):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'details.html', {"month_list": month_year_month_name[0], "year_list": month_year_month_name[2], "month_name": month_year_month_name[1], "shop_details": get_shop_details(request)})


def thankyou(request):
    print(request.session['shop_id'])
    paymentmode = request.POST.get('paymentmode')
    amount = request.POST.get('amount')
    date = request.POST.get('date')
    numberofclient = request.POST.get('numberofclient')
    #get current date and time
    now = datetime.datetime.now()
    datesplit = date.split('-')
    Y = int(datesplit[0])
    m = int(datesplit[1])
    bardate = datetime.datetime(Y, m, 1)
    time = now.strftime('%H:%M:%S')

    customer = ''
    if(paymentmode=='Bharatpe'):
        customer = BharatPe()
    elif(paymentmode=='Paytm'):
        customer = Paytm()
    elif(paymentmode=='Cash'):
        customer = client()
    customer.date = date
    customer.ShopID = request.session['shop_id']
    customer.bardate = bardate
    customer.time = time
    customer.paymentmode = paymentmode
    customer.amount = amount
    customer.numberofclient = numberofclient
    customer.save()
    messages.success(request, 'Added successfully', extra_tags='alert')
    return redirect('/client/details/')


@login_required(login_url="/useraccount/login/")
def membership(request):
    print(request.session['shop_id'])
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    if request.method == "POST":
        membership = Membership()
        membership.custID = request.POST.get('custid')
        membership.shopID = request.session['shop_id']
        membership.Name = request.POST.get('name')
        membership.Sex = request.POST.get('sex')
        membership.Contact_Number = request.POST.get('contact_number')
        membership.DOB = request.POST.get('date')
        membership.save()
        messages.success(request, 'Added successfully', extra_tags='alert')
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'membership.html', {"month_list": month_year_month_name[0], "year_list": month_year_month_name[2], "month_name": month_year_month_name[1], "shop_details": get_shop_details(request)})
