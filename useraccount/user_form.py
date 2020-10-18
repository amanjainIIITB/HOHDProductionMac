from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class OwnerRegistrationForm(UserCreationForm):
    phone = forms.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    Name = forms.CharField()
    class Meta:
        model = get_user_model()
        fields = ['Name', 'phone', 'password1', 'password2']


class AuthenticationForm(forms.Form): # Note: forms.Form NOT forms.ModelForm
    phone = forms.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'}),
        label='Password')

    class Meta:
        fields = ['phone', 'password']