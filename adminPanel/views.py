from django.shortcuts import render, redirect
from staff.models import ShopRegistration
from customer.views import get_all_membership
from messageManagement.views import send_message_to_all_shop_all_owner, send_message_to_all_shop_all_client, send_message_to_particular_shop_all_owner, send_message_to_particular_shop_all_client, send_message_to_particular_shop_specific_client
from .data_export import get_complete_database

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

def send(request):
    if request.method == 'POST':
        shop_id = request.POST.get('shop_id')
        receiver = request.POST.get('receiver')
        greeting_choice = request.POST.get('greeting_choice')
        client_selector = request.POST.get('client_selector')
        greeting = request.POST.get('greeting')
        message = request.POST.get('message')
        if shop_id == "all":
            if receiver == "all":
                # All clients and owners of all shop
                send_message_to_all_shop_all_owner(request, greeting, message)
                send_message_to_all_shop_all_client(request, greeting, message)
            elif receiver == "shop_owner":
                # All owners of all shop
                send_message_to_all_shop_all_owner(request, greeting, message)

            else:
                # All client of all shop
                send_message_to_all_shop_all_client(request, greeting, message)
        else:
            if receiver == "all":
                # All clients and owners of particular shop
                send_message_to_particular_shop_all_owner(request, greeting, message, shop_id)
                send_message_to_particular_shop_all_client(request, greeting, message, shop_id)
            elif receiver == "shop_owner":
                # All owners of particular shop
                send_message_to_particular_shop_all_owner(request, greeting, message, shop_id)
            else:
                if client_selector == "all":
                    # All client of particular shop
                    send_message_to_particular_shop_all_client(request, greeting, message, shop_id)
                else:
                    # Specific client of specific shop
                    send_message_to_particular_shop_specific_client(request, greeting, message, shop_id, client_selector)
    shops = ShopRegistration.objects.values('ShopID', 'Shop_Name', 'Shop_Address')
    return render(request, 'sendMessage.html', {'shops': shops, 
                                                'clients': get_all_membership()})


def exportDB(request):
    return get_complete_database()


def send_email(sender, sender_password, receiver):
    message_greeting = 'Hello '+str(receiver)+','
    message_body='Another testing mail, Please find the statistics Below for the Registered Parlour'
    message_closing = 'Yours truely,\nHouse of Handsomes and Divas'

    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(message_greeting+'\n\n'+message_body+'\n\n'+message_closing)
    msg['Subject'] = 'HOHD Testing Mail'
    msg['From'] = sender
    msg['To'] = receiver

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, sender_password)
    s.send_message(msg)
    s.quit()


def email(request):
    sender='houseofhandsomes@gmail.com'
    sender_password = 'hohrockx@123'
    receivers = ['amanjain2016@gmail.com', 'jain2jain10@gmail.com']
    for receiver in receivers:
        send_email(sender, sender_password, receiver)
    return redirect('/message/send/')


# def send_sms():
#     contacts = '9530101150'
#     routeid = '50'
#     key = '35ED3859DED8C0'
#     campaign = '0'
#     senderid = 'SMSABS'
#     msg = 'Message from the Django Project to the House of Handsomes & Divas'
#     url = 'http://sms.autobysms.com/app/smsapi/index.php?key=' + key + '&campaign=' + campaign + '&routeid=' + routeid + \
#           '&type=text&contacts=' + contacts + '&senderid=' + senderid + '&msg=' + msg
#     response = requests.post(url)