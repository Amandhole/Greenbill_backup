from django.contrib import admin
from .models import *
# Register your models here.

class ParkingLotBillAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'amount', 'green_points_earned','bill_file', 'is_pass')
admin.site.register(SaveParkingLotBill,ParkingLotBillAdmin)
admin.site.register(InvoiceNumberParkingLot,)
admin.site.register(ParkingLotPass,)
admin.site.register(ParkingLog,)

