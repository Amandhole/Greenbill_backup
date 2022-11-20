from django.contrib import admin

# Register your models here.
from .models import OwnerPaymentLinks, SendPaymentManually

admin.site.register(OwnerPaymentLinks) 
admin.site.register(SendPaymentManually) 