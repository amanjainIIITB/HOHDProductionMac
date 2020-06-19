from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json
from staff.models import ShopRegistration
from HOHDProductionMac.common_function import get_month_year_month_name_for_download, atleast_one_shop_registered, \
    get_login_user_shop_details

def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, shop_id):
    if not atleast_one_shop_registered(request):
        return redirect('/staff/shopreg/')
    shop_objs = ShopRegistration.objects.all()
    month_year_month_name = get_month_year_month_name_for_download()
    return render(request, 'chat/room.html', {
        "month_list": month_year_month_name[0],
        "year_list": month_year_month_name[2],
        "month_name": month_year_month_name[1],
        "shop_details": get_login_user_shop_details(request),
        'shop_id': shop_id,
        'username': request.user.username,
        'shop_objs': shop_objs
    })