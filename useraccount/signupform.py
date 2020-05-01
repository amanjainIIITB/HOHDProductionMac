from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class OwnerRegistrationForm(UserCreationForm):
    Contact_Number = forms.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    Name = forms.CharField()
    class Meta:
        model = User
        fields = ['Name', 'Contact_Number', 'username', 'password1', 'password2']
