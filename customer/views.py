from django.shortcuts import render, redirect
from .models import *
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

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

# @login_required(login_url="/useraccount/login/")
def details(request):
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'details.html', {"month_list": month_year_month_name[0], "year_list": month_year_month_name[2], "month_name": month_year_month_name[1]})


def thankyou(request):
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
    customer.bardate = bardate
    customer.time = time
    customer.paymentmode = paymentmode
    customer.amount = amount
    customer.numberofclient = numberofclient
    customer.save()
    messages.success(request, 'Added successfully', extra_tags='alert')
    return redirect('/client/details/')
