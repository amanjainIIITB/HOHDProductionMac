from django.shortcuts import render
import requests
from .utils import *


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
    pass
    # get the data from Access based on the shop_id and isowner
    # owner_ids = Access.objects.values('regID').filter()
    # for owner_id in owner_ids:
    #     owner = get_shop_owner_details_based_on_owner_id(owner_id)
    #     sendMessage(owner['Name'], owner['Contact_Number'], greeting, message, greeting_choice)


def send_message_to_particular_shop_all_client(greeting, message, shop_id, greeting_choice):
    clients = get_clients_details_based_on_shop_id(shop_id)
    for client in clients:
        sendMessage(client['Name'], client['Contact_Number'], greeting, message, greeting_choice)


def send_message_to_particular_shop_specific_client(greeting, message, shop_id, client_id, greeting_choice):
    client = get_client_details_based_on_shop_id_client_id(shop_id, client_id)
    sendMessage(client['Name'], client['Contact_Number'], greeting, message, greeting_choice)




