from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .signupform import OwnerRegistrationForm
from .models import OwnerRegistration
from HOHDProductionMac.common_function import set_session, atleast_one_shop_registered


def signup_view(request):
    if request.method == "POST":
        user_form = OwnerRegistrationForm(request.POST)
        if user_form.is_valid():
            mob = user_form.cleaned_data.get('Contact_Number')
            name = user_form.cleaned_data.get('Name')
            username = user_form.cleaned_data.get('username')
            user_form.save()
            last_owner_id = OwnerRegistration.objects.values('ownerID').last()
            print(last_owner_id)
            new_owner_id = int(str(last_owner_id['ownerID'])[1:])+1
            OwnerRegistration(Name=name, username=username, user=User.objects.filter(username=username).first(), Contact_Number=mob, ownerID='O'+str(new_owner_id), shop_list='None').save()
            return redirect('/client/details/')
    else:
        user_form = OwnerRegistrationForm()
    return render(request, 'signup.html', {'user_form': user_form})


def get_first_shop_id(request):
    ownerIDobj = OwnerRegistration.objects.values('ownerID', 'shop_list').filter(user=str(request.user.id)).first()
    shops = ownerIDobj['shop_list'].split(",")
    return shops[0]


def delete_session(request):
    del request.session['shop_id']


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if atleast_one_shop_registered(request):
                print('Yes shop is registered')
                shop_id = get_first_shop_id(request)
                set_session(request, shop_id)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/staff/aboutus/')
    else:
        form = AuthenticationForm
    return render(request, 'login.html', {'form':form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')