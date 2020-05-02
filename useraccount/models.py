from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class OwnerRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Contact_Number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)], null=True)
    ownerID = models.CharField(max_length=10, null=True)
    Name = models.CharField(max_length=50, null=True)