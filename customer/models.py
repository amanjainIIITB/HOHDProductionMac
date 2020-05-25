import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class client(models.Model):
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    ShopID = models.CharField(max_length=10, default='S1')
    bardate = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    time = models.TimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    numberofclient = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)+" "+str(self.time)


class BharatPe(models.Model):
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    ShopID = models.CharField(max_length=10, default='S1')
    bardate = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    time = models.TimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    numberofclient = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)+" "+str(self.time)


class Paytm(models.Model):
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    ShopID = models.CharField(max_length=10, default='S1')
    bardate = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    time = models.TimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    numberofclient = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)+" "+str(self.time)


class Membership(models.Model):
    custID = models.CharField(max_length=10, null=True)
    shopID = models.CharField(max_length=10, null=True)
    Contact_Number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)],
                                         null=True)
    Sex = models.CharField(max_length=1, null=True)
    Name = models.CharField(max_length=50, null=True)
    DOB = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))