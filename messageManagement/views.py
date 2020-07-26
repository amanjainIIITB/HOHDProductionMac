from django.shortcuts import render
import requests
from .utils import *


# Create your views here.
def sendMessage(receiver_name,receiver_contact_number, greeting, message, greeting_choice):
    routeid = '50'
    key = '35ED3859DED8C0'
    campaign = '0'
    senderid = 'SMSABS'
    if greeting_choice == 'yes':
        message = greeting +" "+receiver_name + ", \n" + message
    print(message)
    url = 'http://sms.autobysms.com/app/smsapi/index.php?key=' + key + '&campaign=' + campaign + '&routeid=' + routeid + \
          '&type=text&contacts=' + str(receiver_contact_number) + '&senderid=' + senderid + '&msg=' + str(message)
    # response = requests.post(url)


def send_message_to_all_shop_all_owner(greeting, message, greeting_choice):
    owners = get_all_shop_owner_details()
    for owner in owners:
        print(owner)
        sendMessage(owner['Name'], owner['Contact_Number'], greeting, message, greeting_choice)


def send_message_to_all_shop_all_client(greeting, message, greeting_choice):
    clients = get_all_clients_details()
    for client in clients:
        sendMessage(client['Name'], client['Contact_Number'], greeting, message, greeting_choice)


def send_message_to_particular_shop_all_owner(greeting, message, shop_id, greeting_choice):
    owner_ids = get_shop_owners_ids_based_on_shop_id(shop_id)['owner_list'].split(",")
    for owner_id in owner_ids:
        owner = get_shop_owner_details_based_on_owner_id(owner_id)
        sendMessage(owner['Name'], owner['Contact_Number'], greeting, message, greeting_choice)


def send_message_to_particular_shop_all_client(greeting, message, shop_id, greeting_choice):
    clients = get_clients_details_based_on_shop_id(shop_id)
    for client in clients:
        sendMessage(client['Name'], client['Contact_Number'], greeting, message, greeting_choice)


def send_message_to_particular_shop_specific_client(greeting, message, shop_id, client_id, greeting_choice):
    client = get_client_details_based_on_shop_id_client_id(shop_id, client_id)
    sendMessage(client['Name'], client['Contact_Number'], greeting, message, greeting_choice)


# def time_interval_message(greeting, shop_id, greeting_choice):
#     days_intervals = [10, 15, 20, 30, 40, 60]
#     for days_interval in days_intervals:
#         event = Event.objects.values('EventID', 'name', 'message', 'date').filter(name=days_interval).first()
#         clients = Membership.objects.values('last_visit', 'Name', 'Contact_Number').filter(shopID=shop_id)
#         for client in clients:
#             if is_date_equal(add_date(client['last_visit'], days_interval), current_date):
#                 # If Client is has exceeded the number of days interval
#                 if is_date_less_than(add_date(event['date'], days_interval), current_date)):
#                     sendMessage(client['Name'], client['Contact_Number'], greeting, event['message'], greeting_choice)
#                 else:
#                     #Update the date of last message to the current date
#                     event = Event.objects.values('EventID', 'name', 'message', 'date').filter(name=days_interval).last()
#                     Event.objects.filter(EventID=event['EventID'])update(date=currentdate)
#                     sendMessage(client['Name'], client['Contact_Number'], greeting, event['message'], greeting_choice)


# def birthday(greeting, shop_id, greeting_choice):
#     event_name='birthday'
#     event = Event.objects.values('EventID', 'name', 'message', 'date').filter(name=event_name).first()
#     clients = Membership.objects.values('DOB', 'Name', 'Contact_Number').filter(shopID=shop_id)
#     for client in clients:
#         if is_date_equal(client['DOB'], event['date']):
#             sendMessage(client['Name'], client['Contact_Number'], greeting, event['message'], greeting_choice)


# def daily_check(request):
#     greeting = 'Hello'
#     greeting_choice = 'no'
#     shop_ids = ShopRegistration.object.values('ShopID', 'Desk_Contact_Number', 'Shop_Name')
#     for shop_id in shop_ids:
#         time_interval_message(greeting, shop_id, greeting_choice)
#         birthday(greeting, shop_id, greeting_choice)
