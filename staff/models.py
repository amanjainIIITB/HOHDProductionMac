from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Expense(models.Model):
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
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

    def __str__(self):
        return str(self.ShopID)


class ShopOwnerRelationship(models.Model):
    ShopID = models.CharField(max_length=10, null=True)
    ownerID = models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.ShopID)+" "+str(self.ownerID)
