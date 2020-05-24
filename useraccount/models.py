from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class OwnerRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Contact_Number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)], null=True)
    username = models.CharField(max_length=50, null=True)
    ownerID = models.CharField(max_length=10, null=True)
    Name = models.CharField(max_length=50, null=True)
    shop_list = models.TextField(null=True)

    def __str__(self):
        return str(self.user)

    def get_username(self):
        return self.user

    def get_name(self):
        return self.Name

    def get_ownerID(self):
        return self.ownerID

    def get_contact_number(self):
        return self.Contact_Number

    def get_shop_list(self):
        return self.shop_list
