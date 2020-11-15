from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
from .models import OwnerRegistration, Access

User = get_user_model()

admin.site.register(User)
admin.site.register(OwnerRegistration)
admin.site.register(Access)