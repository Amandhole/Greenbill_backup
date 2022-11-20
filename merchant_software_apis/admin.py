from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(DeviceId)

class CustomerBillAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'customer_added', 'bill', 'bill_date','bill_amount', 'bill_url','green_points_earned')
admin.site.register(CustomerBill,CustomerBillAdmin)

class MerchantBillAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'bill', 'bill_amount', 'bill_url','customer_added')
admin.site.register(MerchantBill,MerchantBillAdmin)


admin.site.register(InvoiceNumberSoftwareBill)


admin.site.register(ExePrintStatus)