from django.contrib import messages
from datetime import datetime, timedelta
from customer.models import Membership
from useraccount.models import OwnerRegistration, Access
from staff.models import ShopRegistration
from customer.models import ClientVisit, AllService
from django.db.models import Sum, Count, Max
from HOHDProductionMac.settings import ADMIN_PHONE_NUMBER

# Import smtplib for the actual email sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

def get_regID(request, phone_number):
    return OwnerRegistration.objects.values('ownerID').filter(phone=phone_number).first()['ownerID']


def get_all_services():
    all_service_dict = {}
    all_services = AllService.objects.values('ServiceID', 'Name')
    for all_service in all_services:
        number = 0
        character = ''
        for c in all_service['ServiceID']:
            if c >= '0' and c <='9':
                number = number*10 + int(c)
            else:
                character = character + c
        all_service['number'] = number
        all_service['character'] = character
    all_services = list(all_services)
    all_services = sorted(all_services, key=lambda d:(d['character'], d['number']))
    for service_obj in all_services:
        print(service_obj)
        all_service_dict[service_obj['ServiceID']] = service_obj['Name']
    return all_service_dict


def get_services():
    all_services = get_all_services()
    print(all_services)
    services = {}
    hair_services = {}
    face_services = {}
    other_services = {}
    for key, value in all_services.items():
        if 'HS' in key:
            hair_services[key] = value
        elif 'FS' in key:
            face_services[key] = value
        elif 'OS' in key:
            other_services[key] = value
    services['hair'] = hair_services
    services['face'] = face_services
    services['other'] = other_services
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


def atleast_one_shop_registered(request):
    count = Access.objects.filter(regID=request.session['regID']).count()
    if count == 0:
        messages.success(request, 'Register your Shop', extra_tags='alert')
        return False
    else:
        return True


def get_list_of_login_user_shops(request):
    shop_lists = request.session['shop_list_access']
    list_of_shops = []
    for shop_id in shop_lists:
        list_of_shops.append(shop_id)
    print(list_of_shops)
    return list_of_shops


def set_session(request, name, value):
    request.session[name] = value


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


def is_page_accessible(request, function_name):
    if request.session['shop_list_access'][request.session['shop_id']]['isowner'] == False and  request.session['page_permissions_dict'][function_name] not in request.session['shop_list_access'][request.session['shop_id']]['page_list']:
        messages.success(request, request.session['messages']['page_block_error'], extra_tags='alert')
        return False
    return True


def get_login_user_shop_details(request):
    if str(request.user) != 'AnonymousUser' and str(request.user) != ADMIN_PHONE_NUMBER:
        shop_ids = get_list_of_login_user_shops(request)
        list_shop_details = []
        for shopid in shop_ids:
            shop_details = ShopRegistration.objects.values('ShopID', 'Shop_Name', 'Shop_Address').filter(
                ShopID=shopid).last()
            list_shop_details.append(shop_details)
        return list_shop_details
    else:
        return list()


def page_display_dict():
    # Structure = ["Display Name", "Function Name", "Page_id", "Boolean value to decide if you want to display the name"] 

    return {
        "Client Visit:" : [["View", "details", 1, 1], ["Create", "save_mem_visit", 2, 1], ["Create", "save_non_mem_visit", 2, 0], ["Edit", "update_mem_client_visit", 3, 1], ["Edit", "update_non_mem_client_visit", 3, 0], ["Delete", "delete_client_visit", 4, 1]],
        "Client Membership:" : [["View", "membership", 5, 1], ["Create", "create_membership", 6, 1], ["Edit", "update_membership", 7, 1], ["Delete", "delete_membership", 8, 1]],
        "Expense:" : [["View", "expense", 9, 1], ["Create", "add_expense", 10, 1], ["Edit", "update_expense", 11, 1], ["Delete", "delete_expense", 12, 1]],
        "Download files" : [["Analysis Report", "download_analysis_report", 13, 1], ["Expense Data", "download_expense_data", 14, 1], ["Customer Data", "download_customer_data", 15, 1]],
        "Can Employee create Appoint for the Client?" : [["View", "appointment", 16, 1], ["Create/Update", "save_mem_client_appointment", 17, 1], ["Create/Update", "save_non_mem_client_appointment", 17, 0]],
        "Do you want your Employee to see the analytics of your Parlour?" : [["YES", "analysis", 18, 1]],
        "Do you want your Employee to Update the Parlour Details?" : [["Edit Parlour Details", "edit_parlour", 19, 1]],
        "Do you want to provide permission to add Partner for your Parlour?" : [["Add Partner", "add_partner", 20, 1]],
        "Employee" : [["View", "employee", 21, 1], ["Create", "create_employee", 22, 1], ["Edit", "update_employee", 23, 1], ["Delete", "delete_employee", 24, 1]]
    }


def get_page_permission_dict():
    page_permissions_dict = {}
    page_dict = page_display_dict()
    for ques, permissions in page_dict.items():
        for page in permissions:
            print(page)
            page_permissions_dict[page[1]] = str(page[2])
    print(page_permissions_dict)
    return page_permissions_dict


def get_shop_list_access(regID):
    shop_list_access = Access.objects.values('shopID', 'isowner', 'page_list').filter(regID=regID)
    print(list(shop_list_access))
    shop_list_access_json = {}
    for shop_list_access_object in shop_list_access:
        shop_list_access_json[shop_list_access_object['shopID']] = {'isowner': shop_list_access_object['isowner'], 'page_list': shop_list_access_object['page_list'].split(',')}
    return shop_list_access_json


def get_common_attributes(request, attributes_json):
    attributes_json["login_username"] = request.session["login_username"]
    attributes_json["shop_name"] = request.session["shop_name"]
    attributes_json["shop_details"] = request.session["shop_details"]
    attributes_json["shop_list_access"] = request.session["shop_list_access"]
    attributes_json["month_year_month_name"] = request.session["month_year_month_name"]