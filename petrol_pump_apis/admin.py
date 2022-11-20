from django.contrib import admin
from .models import *

class SavePetrolPumpBillAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'amount', 'total_amount', 'green_points_earned')
admin.site.register(SavePetrolPumpBill,SavePetrolPumpBillAdmin)
admin.site.register(InvoiceNumberPetrolPump,)
admin.site.register(PetrolLog,)