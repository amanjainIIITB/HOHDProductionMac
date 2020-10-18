from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class LoginForm(UserCreationForm):
    phone = forms.IntegerField()
    class Meta:
        model = get_user_model()
        fields = ['phone', 'password']

        