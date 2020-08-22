from django.shortcuts import render, redirect
from django.contrib import messages
from staff.models import ShopRegistration
from customer.models import Membership
from customer.views import get_all_membership
from messageManagement.views import send_message_to_all_shop_all_owner, send_message_to_all_shop_all_client, send_message_to_particular_shop_all_owner, send_message_to_particular_shop_all_client, send_message_to_particular_shop_specific_client
from .data_export import get_complete_database
from .models import Event
from HOHDProductionMac.common_function import get_all_membership_based_on_shop_id, get_month_year_month_name_for_download, get_login_user_shop_details, get_current_date, add_date, is_date_less, is_date_and_month_equal
import datetime


# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage


def get_new_event_id(request):
    last_event_id = Event.objects.values('EventID').last()
    if last_event_id == None:
        return 'Event0'
    else:
        new_event_id = 'Event' + str(int(str(last_event_id['EventID'])[5:]) + 1)
        return new_event_id


def addevent(request):
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
    return get_complete_database()


def send_email(message_body):
    sender='houseofhandsomes@gmail.com'
    receivers = ['amanjain2016@gmail.com']
    for receiver in receivers:
        message_greeting = 'Hello '+str(receiver)+','
        message_opening = 'Please find the statistics Below for the Registered Parlour'
        message_closing = 'Yours truely,\nHouse of Handsomes and Divas'

        # Create a text/plain message
        msg = EmailMessage()
        msg.set_content(message_greeting+'\n\n'+message_opening+'\n\n'+message_body+'\n\n'+message_closing)
        msg['Subject'] = 'Message Report'
        msg['From'] = sender
        msg['To'] = receiver

        # Send the message via our own SMTP server.
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender, 'hohrockx@123')
        s.send_message(msg)
        s.quit()


def email(request):
    message_body = 'Testing Mail'
    for receiver in receivers:
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
            date = datetime.datetime.strptime(client['last_visit'], "%Y-%m-%d")
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