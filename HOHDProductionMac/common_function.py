from django.contrib import messages
import datetime
from useraccount.models import OwnerRegistration
from staff.models import ShopRegistration

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


def atleast_one_shop_registered(request):
    ownerIDobj = OwnerRegistration.objects.values('ownerID', 'shop_list').filter(user=str(request.user.id)).first()
    print(ownerIDobj)
    if ownerIDobj['shop_list'] == 'None':
        print('I am inside the empty list')
        messages.success(request, 'Register your Parlour or ask your partner to add you', extra_tags='alert')
        return False
    else:
        return True


def get_list_of_login_user_shops(request):
    ownerIDobj = OwnerRegistration.objects.values('ownerID', 'shop_list').filter(user=str(request.user.id)).first()
    return ownerIDobj['shop_list'].split(",")


def get_login_user_shop_details(request):
    shops = get_list_of_login_user_shops(request)
    list_shop_details = []
    for shopid in shops:
        shop_details = ShopRegistration.objects.values('ShopID', 'Shop_Name', 'Shop_Address').filter(
            ShopID=shopid).last()
        list_shop_details.append(shop_details)
    return list_shop_details


def set_session(request, shop_id):
    request.session['shop_id'] = shop_id
