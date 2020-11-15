from datetime import datetime
from staff.models import ShopRegistration
from HOHDProductionMac.common_function import get_list_of_login_user_shops
from staff.models import Expense, ShopRegistration


DB_PHONE_NUMBER = '0246813579'
def get_month_year_month_name_for_download(request):
    now = datetime.now()
    month_year_month_name = {}
    month_index = []
    year_list = []
    month_name = []
    index_to_month_name = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov',
                            'Dec']
    current_month = now.month
    current_year = now.year
    for i in range(4):
        if current_month == 0:
            current_month = 12
            current_year = current_year - 1
        month_index.append(current_month)
        month_name.append(index_to_month_name[current_month - 1])
        year_list.append(current_year)
        current_month = current_month - 1
    month_year_month_name['month_index'] = month_index
    month_year_month_name['month_name'] = month_name
    month_year_month_name['year_list'] = year_list
    return {"month_year_month_name" : month_year_month_name}

def get_login_user_shop_details(request):
    if str(request.user) != 'AnonymousUser' and str(request.user) != DB_PHONE_NUMBER:
        shop_ids = get_list_of_login_user_shops(request)
        list_shop_details = []
        for shopid in shop_ids:
            shop_details = ShopRegistration.objects.values('ShopID', 'Shop_Name', 'Shop_Address').filter(
                ShopID=shopid).last()
            list_shop_details.append(shop_details)
        return {"shop_details" : list_shop_details}
    else:
        return {}

def get_login_username(request):
    if str(request.user) != 'AnonymousUser' and str(request.user) != DB_PHONE_NUMBER:
        return {"login_username": request.user.get_phone_number()}
    else:
        return {}

def get_shop_name(request):
    if str(request.user) != 'AnonymousUser' and str(request.user) != DB_PHONE_NUMBER:
        return {"shop_name": ShopRegistration.objects.values('Shop_Name').filter(ShopID=request.session['shop_id']).first()['Shop_Name']}
    else:
        return {}