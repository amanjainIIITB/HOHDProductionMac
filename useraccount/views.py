from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .user_form import OwnerRegistrationForm, AuthenticationForm
from .models import OwnerRegistration, Access
from staff.models import ShopRegistration
from HOHDProductionMac.common_function import set_session, atleast_one_shop_registered, get_regID, get_page_permission_dict, get_login_user_shop_details, get_shop_list_access
from HOHDProductionMac.settings import ADMIN_PHONE_NUMBER
from datetime import datetime


def profile_details(request):
    if request.method == 'POST':
        pass
    return render(request, 'profile_details.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form })


def create_owner_registration(name, phone):
    last_owner_id = OwnerRegistration.objects.values('ownerID').last()
    new_owner_id = ''
    if last_owner_id is None:
        new_owner_id = '0'
    else:
        new_owner_id = int(str(last_owner_id['ownerID'])[1:])+1
    OwnerRegistration(Name=name, phone=phone, ownerID='O'+str(new_owner_id)).save()


def signup_view(request):
    if request.method == "POST":
        user_form = OwnerRegistrationForm(request.POST) 
        if user_form.is_valid():
            mob = user_form.cleaned_data.get('phone')
            name = user_form.cleaned_data.get('Name')
            user_form.save()
            create_owner_registration(name, mob)
            return redirect('/')
        else:
            phone_length = len(request.POST['phone'])
            if len(user_form.cleaned_data.get('password1')) < 8:
                messages.success(request, 'Password should not be less than 8 character', extra_tags='alert')
            elif request.POST['password1'] != request.POST['password2']:
                messages.success(request, 'Password and confirm password are not same', extra_tags='alert')
            elif phone_length > 10:
                messages.success(request, 'Phone Number cannot be more than 10 digit', extra_tags='alert')
            elif phone_length < 10:
                messages.success(request, 'Phone Number cannot be less than 10 digit', extra_tags='alert')
            else:
                messages.success(request, 'Signup Failed, Please Contact Administrator', extra_tags='alert')
    else:
        user_form = OwnerRegistrationForm()
    return render(request, 'signup.html', {'user_form': user_form})


def get_first_shop_id(regID):
    return Access.objects.values('shopID').filter(regID=regID).first()['shopID']


def get_first_shop_name(request):
    if request.session['shop_id'] == None:
        return "Shop does Not Exist"
    else:
        return ShopRegistration.objects.values('Shop_Name').filter(ShopID=request.session['shop_id']).first()['Shop_Name']


def delete_session(request):
    del request.session['shop_id']


def get_login_username(request):
    if request!=None and str(request.user) != 'AnonymousUser' and str(request.user) != ADMIN_PHONE_NUMBER:
        return request.user.get_phone_number()
    else:
        return "invalid_username"


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
    return month_year_month_name


def get_messages():
    return {'page_block_error': 'This Page has been blocked by the owner'}


def get_login_session_report(request):
    login_session_report = {
        'Name of the Report' : 'get_login_session_report',
        'regID' : request.session['regID'],
        'atleast_one_shop_registered' : atleast_one_shop_registered(request),
        'login_username' : get_login_username(request),
        'month_year_month_name' : get_month_year_month_name_for_download(request),
        'shop_id' : request.session['shop_id'],
        'shop_name' : get_first_shop_name(request),
        'shop_list_access' : request.session['shop_list_access'],
        'shop_details' : get_login_user_shop_details(request)
    }
    if atleast_one_shop_registered(request):
        login_session_report['page_permissions_dict'] = request.session['page_permissions_dict']
        login_session_report['messages'] = request.session['messages']
    print(login_session_report)


def set_login_session(request, phone):
    set_session(request, "regID", OwnerRegistration.objects.values('ownerID').filter(phone=phone).first()['ownerID'])
    set_session(request, "login_username", get_login_username(request))
    set_session(request, "month_year_month_name", get_month_year_month_name_for_download(request))
    if 'next' in request.POST:
        return redirect(request.POST.get('next'))
    if atleast_one_shop_registered(request):
        print('Yes shop is registered')
        shop_id = get_first_shop_id(request.session['regID'])
        set_session(request, "shop_id", shop_id)
        set_session(request, "shop_list_access", get_shop_list_access(request.session['regID']))
        set_session(request, "page_permissions_dict", get_page_permission_dict())
        set_session(request, "messages", get_messages())
    else:
        set_session(request, "shop_id",None)
        set_session(request, "shop_list_access", '')
    set_session(request, 'shop_name', get_first_shop_name(request))
    set_session(request, 'shop_details', get_login_user_shop_details(request))
    get_login_session_report(request)


def login_post(request):
    login_form = AuthenticationForm(data=request.POST)
    if login_form.is_valid():
        user = authenticate(phone = request.POST['phone'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            set_login_session(request, request.user.phone)
            return redirect('/staff/aboutus/')
        else:
            messages.success(request, 'Either Phone Number or Password is incorrect', extra_tags='alert')
    else:
        phone_length = len(request.POST['phone'])
        if phone_length > 10:
            messages.success(request, 'Phone Number cannot be more than 10 digit', extra_tags='alert')
        elif phone_length < 10:
            messages.success(request, 'Phone Number cannot be less than 10 digit', extra_tags='alert')
        else:
            messages.success(request, 'Phone Number is not registered', extra_tags='alert')
    return render(request, 'login.html', {'form':login_form})


def login_view(request):
    logout(request)
    login_form = AuthenticationForm()
    return render(request, 'login.html', {'form':login_form})


def logout_view(request):
    logout(request)
    return redirect('/')