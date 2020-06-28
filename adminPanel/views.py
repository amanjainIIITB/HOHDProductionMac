from django.shortcuts import render
from staff.models import ShopRegistration
from customer.views import get_all_membership
from messageManagement.views import send_message_to_all_shop_all_owner, send_message_to_all_shop_all_client, send_message_to_particular_shop_all_owner, send_message_to_particular_shop_all_client, send_message_to_particular_shop_specific_client


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