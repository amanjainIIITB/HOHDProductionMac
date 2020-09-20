from django.contrib import messages
from datetime import datetime, timedelta
from customer.models import Membership
from useraccount.models import OwnerRegistration
from staff.models import ShopRegistration
from customer.models import ClientVisit, AllService
from django.db.models import Sum, Count, Max

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage


def get_all_services():
    all_service_dict = {}
    all_service = AllService.objects.all()
    for service_obj in all_service:
        all_service_dict[service_obj.ServiceID] = service_obj.Name
    return all_service_dict


def get_services():
    all_services = get_all_services()
    services = {}
    services['hair'] = {'S1': all_services['S1'], 'S2': all_services['S2'], 'S3': all_services['S3'], 'S4': all_services['S4'], 'S5': all_services['S5'], 'S6': all_services['S6'], 'S7': all_services['S7'], 'S8': all_services['S8'], 'S9': all_services['S9'], 'S10': all_services['S10'], 'S11': all_services['S11'], 'S12': all_services['S12']}
    services['face'] = {'S13': all_services['S13'], 'S14': all_services['S14'], 'S15': all_services['S15'], 'S16': all_services['S16']}
    services['other'] = {'S17': all_services['S17'], 'S18': all_services['S18'], 'S19': all_services['S19'], 'S20': all_services['S20'], 'S21': all_services['S21'], 'S22': all_services['S22']}
    return services

    
def convert_date_yyyy_mm_dd_to_dd_mm_yyyy(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime("%d-%b-%Y")

def convert_date_dd_mm_yyyy_to_yyyy_mm_dd(date):
    return datetime.strptime(date, "%d-%b-%Y").strftime("%Y-%m-%d")

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


def is_date_and_month_equal(date1, date2):
    date1split = str(date1).split("-")
    date2split = date2.split("-")
    return date1split[2]==date2split[2] and date1split[1]==date2split[1]


def is_month_and_year_equal(date1, date2):
    date1split = str(date1).split("-")
    date2split = date2.split("-")
    return date1split[0]==date2split[0] and date1split[1]==date2split[1]


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


def get_all_membership_based_on_shop_id(request, ShopID):
    client_visit_group_by_client_id = ClientVisit.objects.values('custID', 'date').filter(ShopID=ShopID).annotate(sum_amount=Sum('amount'), count_number_of_visit=Count('custID'), last_date=Max('date'))
    client_visit_group_by_client_id_dict_key_clientID = {}
    for client_visit_obj in client_visit_group_by_client_id:
        client_visit_group_by_client_id_dict_key_clientID.update({client_visit_obj['custID'] : client_visit_obj})
    memberships = Membership.objects.values('custID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit').filter(shopID=ShopID)
    for membership in memberships:
        if membership['DOB'] != '':
            print(membership['DOB'])
            membership['DOB'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(membership['DOB'])
        if membership['custID'] not in client_visit_group_by_client_id_dict_key_clientID.keys():
            membership['last_visit'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(membership['last_visit'].strftime("%Y-%m-%d"))
        else:
            membership['last_visit'] = convert_date_yyyy_mm_dd_to_dd_mm_yyyy(client_visit_group_by_client_id_dict_key_clientID[membership['custID']]['date'].strftime("%Y-%m-%d"))
        if membership['custID'] not in client_visit_group_by_client_id_dict_key_clientID.keys() or client_visit_group_by_client_id_dict_key_clientID[membership['custID']]['sum_amount'] == 0 or client_visit_group_by_client_id_dict_key_clientID[membership['custID']]['count_number_of_visit'] == 0:
            membership['avg'] = 0
        else:
            membership['avg'] = round(client_visit_group_by_client_id_dict_key_clientID[membership['custID']]['sum_amount']/client_visit_group_by_client_id_dict_key_clientID[membership['custID']]['count_number_of_visit'], 2)
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
    return memberships


def email_format(message_body, sender, receiver, subject, Name):
    message_greeting = 'Hello '+str(Name)+','
    message_closing = 'Yours truely,\nHouse of Handsomes and Divas'

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(message_greeting+'\n\n'+message_body+'\n\n'+message_closing)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, 'hohrockx@123')
    s.send_message(msg)
    s.quit()
