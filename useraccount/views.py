from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .user_form import OwnerRegistrationForm, AuthenticationForm
from .models import OwnerRegistration, Access
from HOHDProductionMac.context_processor import get_page_permission_dict, get_messages
from HOHDProductionMac.common_function import set_session, atleast_one_shop_registered, get_first_shop_name, get_regID


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


def get_first_shop_id(request):
    return Access.objects.values('shopID').filter(regID=request.session['regID']).first()['shopID']


def delete_session(request):
    del request.session['shop_id']


def get_shop_list_access(request):
    shop_list_access = Access.objects.values('shopID', 'isowner', 'page_list').filter(regID=request.session['regID'])
    print(list(shop_list_access))
    shop_list_access_json = {}
    for shop_list_access_object in shop_list_access:
        shop_list_access_json[shop_list_access_object['shopID']] = {'isowner': shop_list_access_object['isowner'], 'page_list': shop_list_access_object['page_list'].split(',')}
    return shop_list_access_json


def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(phone = request.POST['phone'], password = request.POST['password'])
            if user is not None:
                login(request, user)
                set_session(request, "regID", OwnerRegistration.objects.values('ownerID').filter(phone=request.user.phone).first()['ownerID'])
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                if atleast_one_shop_registered(request):
                    print('Yes shop is registered')
                    shop_id = get_first_shop_id(request)
                    set_session(request, "shop_id", shop_id)
                    set_session(request, "shop_list_access", get_shop_list_access(request))
                    set_session(request, "page_permissions_dict", get_page_permission_dict(request))
                    set_session(request, "messages", get_messages(request))
                else:
                    set_session(request, "shop_id",None)
                    set_session(request, "shop_list_access", '')
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
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'form':login_form})


def logout_view(request):
    logout(request)
    return redirect('/')