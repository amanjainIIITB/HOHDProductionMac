import datetime

from django.db import models

# Create your models here.
class client(models.Model):
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    bardate = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    time = models.TimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    numberofclient = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)+" "+str(self.time)

class BharatPe(models.Model):
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    bardate = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    time = models.TimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    numberofclient = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)+" "+str(self.time)

class Paytm(models.Model):
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    bardate = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    time = models.TimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    numberofclient = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)+" "+str(self.time)