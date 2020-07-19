import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class ClientVisit(models.Model):
    visitID = models.CharField(max_length=10, null=True)
    isMember = models.BooleanField(default=False)
    custID = models.CharField(max_length=10, default='None')
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    employee_id = models.CharField(max_length=50, null=True)
    payment_mode = models.CharField(max_length=50, null=True)
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
    last_visit = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    total_amount = models.IntegerField(default=0)
    number_of_visit = models.IntegerField(default=0)

    def __str__(self):
        return str(self.DOB)