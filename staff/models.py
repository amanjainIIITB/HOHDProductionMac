from django.db import models
import datetime

# Create your models here.
class Expense(models.Model):
    date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))
    purpose = models.CharField(max_length=100, null=True)
    paymentmode = models.CharField(max_length=100, null=True)
    comment = models.CharField(max_length=1000, null=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)