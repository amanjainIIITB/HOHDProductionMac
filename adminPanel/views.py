from django.shortcuts import render, redirect
from django.contrib import messages
from staff.models import ShopRegistration
from customer.models import Membership
from customer.views import get_all_membership
from messageManagement.views import send_message_to_all_shop_all_owner, send_message_to_all_shop_all_client, send_message_to_particular_shop_all_owner, send_message_to_particular_shop_all_client, send_message_to_particular_shop_specific_client
from .data_export import get_complete_database
from .data_import import put_complete_database
from .data_delete import delete_complete_database
from .models import Event
from HOHDProductionMac.common_function import get_all_membership_based_on_shop_id, get_current_date, add_date, is_date_less, is_date_and_month_equal, email_format, convert_date_dd_mm_yyyy_to_yyyy_mm_dd
import datetime


def get_new_event_id(request):
    last_event_id = Event.objects.values('EventID').last()
    if last_event_id == None:
        return 'Event0'
    else:
        new_event_id = 'Event' + str(int(str(last_event_id['EventID'])[5:]) + 1)
        return new_event_id


def addevent(request):
    if request.user.get_phone_number() != '0246813579':
        return render(request, 'notAllowed.html')
    if request.method == "POST":
        event_id=get_new_event_id(request)
        Event(EventID=event_id, name=request.POST.get('name'), message=request.POST.get('message')).save()
        messages.success(request, 'Added successfully', extra_tags='alert')
    events = Event.objects.values('EventID', 'name', 'message', 'date')
    return render(request, 'addevent.html')


def create_message_body(occasion, membership_count, message):
    message_body = 'sent '+str(occasion)+' message to '+str(membership_count)+' Client' '\n'
    message_body = message_body + 'Message: '+str(message) + '\n'
    message_body = message_body + '\n'
    return message_body


def email_particular_shop_all_clients(occasion, shop_detail, count, message):
    message_body = str(shop_detail['ShopID']) +'-'+str(shop_detail['Shop_Name'])+'\n'
    message_body = message_body + create_message_body(occasion, count, message)
    return message_body

    
def email_all_shops_all_clients(occasion, message):
    shop_details = ShopRegistration.objects.values('ShopID', 'Shop_Name')
    message_body = ''
    for shop_detail in shop_details:
        membership_count = Membership.objects.filter(shopID=shop_detail['ShopID']).count()
        message_body = message_body + email_particular_shop_all_clients(occasion, shop_detail, membership_count, message)
    print(message_body)
    send_email(message_body)


def send(request):
    if request.user.get_phone_number() != '0246813579':
        return render(request, 'notAllowed.html')
    if request.method == 'POST':
        shop_id = request.POST.get('shop_id')
        receiver = request.POST.get('receiver')
        greeting_choice = request.POST.get('greeting_choice')
        client_selector = request.POST.get('client_selector')
        greeting = request.POST.get('greeting')
        occasion = request.POST.get('occasion')
        message = request.POST.get('message')
        if shop_id == "all":
            if receiver == "all":
                # All clients and owners of all shop
                send_message_to_all_shop_all_owner(greeting, message, greeting_choice)
                email_all_shops_all_clients(occasion, message)
                send_message_to_all_shop_all_client(greeting, message, greeting_choice)
            elif receiver == "shop_owner":
                # All owners of all shop
                send_message_to_all_shop_all_owner(greeting, message, greeting_choice)
            else:
                # All client of all shop
                email_all_shops_all_clients(occasion, message)
                send_message_to_all_shop_all_client(greeting, message, greeting_choice)
        else:
            shop_detail = ShopRegistration.objects.values('ShopID', 'Shop_Name').filter(ShopID=shop_id).first()
            if receiver == "all":
                # All clients and owners of particular shop
                send_message_to_particular_shop_all_owner(greeting, message, shop_id, greeting_choice)
                membership_count = Membership.objects.filter(shopID=shop_detail['ShopID']).count()
                send_email(email_particular_shop_all_clients(occasion, shop_detail, membership_count, message))
                send_message_to_particular_shop_all_client(greeting, message, shop_id, greeting_choice)
            elif receiver == "shop_owner":
                # All owners of particular shop
                send_message_to_particular_shop_all_owner(greeting, message, shop_id, greeting_choice)
            else:
                if client_selector == "all":
                    # All client of particular shop
                    membership_count = Membership.objects.filter(shopID=shop_detail['ShopID']).count()
                    send_email(email_particular_shop_all_clients(occasion, shop_detail, membership_count, message))
                    send_message_to_particular_shop_all_client(greeting, message, shop_id, greeting_choice)
                else:
                    # Specific client of specific shop
                    send_message_to_particular_shop_specific_client(greeting, message, shop_id, client_selector, greeting_choice)
    shops = ShopRegistration.objects.values('ShopID', 'Shop_Name', 'Shop_Address')
    event_names = Event.objects.values('name').order_by('name').distinct
    return render(request, 'sendMessage.html', {'shops': shops, 'event_names': event_names,
                                                'clients': get_all_membership()})


def exportDB(request):
    if request.user.get_phone_number() != '0246813579':
        return render(request, 'notAllowed.html')
    return get_complete_database()

def deleteDB(request):
    if request.user.get_phone_number() != '0246813579':
        return render(request, 'notAllowed.html')
    delete_complete_database()
    return redirect('/message/send/')

def importDB(request):
    if request.user.get_phone_number() != '0246813579':
        return render(request, 'notAllowed.html')
    if request.method == 'POST':
        print(request)
        print(request.FILES.get('import'))
        put_complete_database(request.FILES.get('import'))
        messages.success(request, 'Uploaded successfully', extra_tags='alert')
    return render(request, 'import.html')


def send_email(message_body):
    if request.user.get_phone_number() != '0246813579':
        return render(request, 'notAllowed.html')
    sender='houseofhandsomes@gmail.com'
    receivers = ['amanjain2016@gmail.com']
    for receiver in receivers:
        message_body = 'Please find the statistics Below for the Registered Parlour\n\n'+message_body
        email_format(message_body, sender, receiver, 'Message Report', receiver)


def email(request):
    if request.user.get_phone_number() != '0246813579':
        return render(request, 'notAllowed.html')
    message_body = 'Testing Mail'
    send_email(message_body)
    return redirect('/message/send/')


def time_interval_message(request, greeting, shop_detail, greeting_choice):
    days_intervals = [10, 15, 20, 30, 45, 60]
    message_body = ''
    for days_interval in days_intervals:
        count = 0
        event = Event.objects.values('EventID', 'name', 'message', 'date').filter(name=days_interval).order_by('date').first()
        clients = get_all_membership_based_on_shop_id(request, shop_detail['ShopID'])
        for client in clients:
            date = datetime.datetime.strptime(convert_date_dd_mm_yyyy_to_yyyy_mm_dd(client['last_visit']), "%Y-%m-%d")
            if str(add_date(date, int(days_interval))).split()[0] == str(get_current_date()):
                count = count + 1
                # If Client is has exceeded the number of days interval
                if is_date_less(add_date(event['date'], days_interval), get_current_date()):
                    #Update the date of last message to the current date
                    event = Event.objects.values('EventID', 'name', 'message', 'date').filter(name=days_interval).order_by('date').last()
                    Event.objects.filter(EventID=event['EventID']).update(date=get_current_date())
                send_message_to_particular_shop_specific_client(greeting, event['message'], shop_detail['ShopID'], client['custID'], greeting_choice)
        message_body = message_body + create_message_body(event['name']+' days interval', count, event['message'])
    return message_body


def birthday(request, greeting, shop_detail, greeting_choice):
    event_name='Birthday'
    count = 0
    event = Event.objects.values('EventID', 'name', 'message', 'date').filter(name=event_name).first()
    clients = get_all_membership_based_on_shop_id(request, shop_detail['ShopID'])
    for client in clients:
        if str(client['DOB']) != '' and is_date_and_month_equal(client['DOB'], get_current_date()):
            count = count + 1
            send_message_to_particular_shop_specific_client(greeting, event['message'], shop_detail['ShopID'], client['custID'], greeting_choice)
    return create_message_body(event['name'], count, event['message'])


def daily_check(request):
    if request.user.get_phone_number() != '0246813579':
        return render(request, 'notAllowed.html')
    greeting = 'Hello'
    greeting_choice = 'no'
    message_body = ''
    shop_details = ShopRegistration.objects.values('ShopID', 'Desk_Contact_Number', 'Shop_Name')
    for shop_detail in shop_details:
        message_body = message_body + str(shop_detail['ShopID']) +'-'+str(shop_detail['Shop_Name'])+'\n'
        message_body = message_body + time_interval_message(request, greeting, shop_detail, greeting_choice)
        message_body = message_body + birthday(request, greeting, shop_detail, greeting_choice)
    send_email(message_body)
    return redirect('/message/send/')