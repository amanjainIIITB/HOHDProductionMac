from datetime import datetime
from staff.models import ShopRegistration
from HOHDProductionMac.common_function import get_list_of_login_user_shops
from staff.models import Expense, ShopRegistration


ADMIN_PHONE_NUMBER = '0246813579'

def get_month_year_month_name_for_download(request):
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
    return {"month_year_month_name" : month_year_month_name}

def get_login_user_shop_details(request):
    if str(request.user) != 'AnonymousUser' and str(request.user) != ADMIN_PHONE_NUMBER:
        shop_ids = get_list_of_login_user_shops(request)
        list_shop_details = []
        for shopid in shop_ids:
            shop_details = ShopRegistration.objects.values('ShopID', 'Shop_Name', 'Shop_Address').filter(
                ShopID=shopid).last()
            list_shop_details.append(shop_details)
        return {"shop_details" : list_shop_details}
    else:
        return {}

def get_login_username(request):
    if str(request.user) != 'AnonymousUser' and str(request.user) != ADMIN_PHONE_NUMBER:
        return {"login_username": request.user.get_phone_number()}
    else:
        return {}

def get_shop_name(request):
    if str(request.user) != 'AnonymousUser' and str(request.user) != ADMIN_PHONE_NUMBER and request.session['shop_id'] != None:
        return {"shop_name": ShopRegistration.objects.values('Shop_Name').filter(ShopID=request.session['shop_id']).first()['Shop_Name']}
    else:
        return {}

def page_display_dict():
    # Structure = ["Display Name", "Function Name", "Page_id", "Boolean value to decide if you want to display the name"] 

    return {
        "Client Visit:" : [["View", "details", 1, 1], ["Create", "save_mem_visit", 2, 1], ["Create", "save_non_mem_visit", 2, 0], ["Edit", "update_mem_client_visit", 3, 1], ["Edit", "update_non_mem_client_visit", 3, 0], ["Delete", "delete_client_visit", 4, 1]],
        "Client Membership:" : [["View", "membership", 5, 1], ["Create", "create_membership", 6, 1], ["Edit", "update_membership", 7, 1], ["Delete", "delete_membership", 8, 1]],
        "Expense:" : [["View", "expense", 9, 1], ["Create", "add_expense", 10, 1], ["Edit", "update_expense", 11, 1], ["Delete", "delete_expense", 12, 1]],
        "Download files" : [["Analysis Report", "download_analysis_report", 13, 1], ["Expense Data", "download_expense_data", 14, 1], ["Customer Data", "download_customer_data", 15, 1]],
        "Can Employee create Appoint for the Client?" : [["View", "appointment", 16, 1], ["Create/Update", "save_mem_client_appointment", 17, 1], ["Create/Update", "save_non_mem_client_appointment", 17, 0]],
        "Do you want your Employee to see the analytics of your Parlour?" : [["", "analysis", 18, 1]],
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

def get_messages():
    return {'page_block_error': 'This Page has been blocked by the owner'}