from customer.models import Membership
from useraccount.models import OwnerRegistration
from staff.models import ShopRegistration


def get_shop_owner_details_based_on_owner_id(owner_id):
    return OwnerRegistration.objects.values('phone', 'ownerID', 'Name').filter(ownerID=owner_id).first()


def get_all_shop_owner_details():
    return OwnerRegistration.objects.values('phone', 'ownerID', 'Name', 'shop_list')


def get_client_details_based_on_shop_id_client_id(shop_id, client_id):
    return Membership.objects.values('custID', 'shopID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit').filter(shopID=shop_id, custID=client_id).first()


def get_clients_details_based_on_shop_id(shop_id):
    return Membership.objects.values('custID', 'shopID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit').filter(shopID=shop_id)


def get_all_clients_details():
    return Membership.objects.values('custID', 'shopID', 'Contact_Number', 'Sex', 'Name', 'DOB', 'last_visit')

