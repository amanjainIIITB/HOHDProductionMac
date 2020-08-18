from django.contrib import messages
from datetime import datetime, timedelta
from customer.models import Membership
from useraccount.models import OwnerRegistration
from staff.models import ShopRegistration


def get_current_time():
    # current date and time
    return (datetime.now() + timedelta(hours=5, minutes=30)).strftime("%H:%M:%S")


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def add_date(date, days):
    return date + timedelta(days=days)


def get_current_date_time():
    return str(get_current_date())+" "+str(get_current_time())


def is_date_greater(date1, date2):
    date1split = str(date1).split("-")
    date2split = date2.split("-")
    return datetime(int(date1split[0]), int(date1split[1]), int(date1split[2])) > datetime(int(date2split[0]), int(date2split[1]), int(date2split[2]))


def is_date_less(date1, date2):
    date1split = str(date1).split("-")
    date2split = date2.split("-")
    return datetime(int(date1split[0]), int(date1split[1]), int(date1split[2])) < datetime(int(date2split[0]), int(date2split[1]), int(date2split[2]))


def get_month_year_month_name_for_download():
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
    return month_year_month_name


def atleast_one_shop_registered(request):
    ownerIDobj = OwnerRegistration.objects.values('ownerID', 'shop_list').filter(user=str(request.user.id)).first()
    if ownerIDobj['shop_list'] == 'None':
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


def get_all_membership_based_on_shop_id(request):
    memberships = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit', 'total_amount', 'number_of_visit').filter(shopID=request.session['shop_id'])
    for membership in memberships:
        membership['DOB'] = membership['DOB']
        membership['last_visit'] = membership['last_visit'].strftime("%Y-%m-%d")
        if membership['total_amount'] == 0 or membership['number_of_visit'] == 0:
            membership['avg'] = 0
        else:
            membership['avg'] = round(membership['total_amount']/membership['number_of_visit'], 2)
        custID_number = 0
        custID_character = ''
        for c in membership['custID']:
            if c >= '0' and c <='9':
                custID_number = custID_number*10 + int(c)
            else:
                custID_character = custID_character + c
        membership['custID_number'] = custID_number
        membership['custID_character'] = custID_character
    memberships = list(memberships)
    memberships = sorted(memberships, key=lambda d:(d['custID_character'], d['custID_number']))
    print(memberships)
    return memberships
