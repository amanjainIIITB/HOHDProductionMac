from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Expense(models.Model):
    ExpenseID = models.CharField(max_length=10, default='E1')
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    shopID = models.CharField(max_length=10, default='S1')
    purpose = models.CharField(max_length=100, null=True)
    paymentmode = models.CharField(max_length=100, null=True)
    comment = models.CharField(max_length=1000, null=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)


class ShopRegistration(models.Model):
    ShopID = models.CharField(max_length=10, null=True)
    Desk_Contact_Number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)],
                                              null=True)
    Shop_Name = models.CharField(max_length=50, null=True)
    Shop_Address = models.CharField(max_length=200, null=True)
    owner_list = models.TextField(null=True)

    def __str__(self):
        return str(self.ShopID)


class Employee(models.Model):
    EmployeeID = models.CharField(max_length=10, null=True)
    ShopID = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=50, null=True)
    contact_number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)],
                                              null=True)
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=10, null=True)
    date_of_joining = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    DOB = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    temporary_address = models.TextField(max_length=1000, null=True)
    permanent_address = models.TextField(max_length=1000, null=True)
