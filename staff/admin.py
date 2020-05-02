from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Expense)
admin.site.register(ShopRegistration)
admin.site.register(ShopOwnerRelationship)