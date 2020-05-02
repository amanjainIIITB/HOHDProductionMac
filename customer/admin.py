from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(client)
admin.site.register(BharatPe)
admin.site.register(Paytm)
admin.site.register(Membership)