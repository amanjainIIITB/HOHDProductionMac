from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .user_form import OwnerRegistrationForm, AuthenticationForm
from .models import OwnerRegistration
from HOHDProductionMac.common_function import set_session, atleast_one_shop_registered, get_month_year_month_name_for_download, get_first_shop_name

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
    return render(request, 'change_password.html', {"month_year_month_name": get_month_year_month_name_for_download(),
                                                    "login_username": request.user.get_username(),
                                                    'shop_name': get_first_shop_name(request),
                                                    'form': form })


def signup_view(request):
    if request.method == "POST":
        user_form = OwnerRegistrationForm(request.POST) 
        if user_form.is_valid():
            mob = user_form.cleaned_data.get('phone')
            name = user_form.cleaned_data.get('Name')
            user_form.save()
            last_owner_id = OwnerRegistration.objects.values('ownerID').last()
            new_owner_id = ''
            if last_owner_id is None:
                new_owner_id = '0'
            else:
                new_owner_id = int(str(last_owner_id['ownerID'])[1:])+1
            OwnerRegistration(Name=name, phone=mob, ownerID='O'+str(new_owner_id)).save()
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
    ownerIDobj = OwnerRegistration.objects.values('ownerID', 'shop_list').filter(phone=request.user.get_phone_number()).first()
    shops = ownerIDobj['shop_list'].split(",")
    return shops[0]


def delete_session(request):
    del request.session['shop_id']


def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(phone = request.POST['phone'], password = request.POST['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                if atleast_one_shop_registered(request):
                    print('Yes shop is registered')
                    shop_id = get_first_shop_id(request)
                    set_session(request, shop_id)
                else:
                    set_session(request, None)
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