from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(ClientVisit)
admin.site.register(Membership)
admin.site.register(Services)
admin.site.register(AllService)