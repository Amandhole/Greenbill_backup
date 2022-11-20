from django.contrib import admin
from .models import *

class CustomerCashMemoDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'memo_url')

admin.site.register(CustomerCashMemoDetailModels,CustomerCashMemoDetailAdmin)

class CustomerReceiptDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'receipt_url')
admin.site.register(CustomerReceiptDetailsModels,CustomerReceiptDetailsAdmin)


admin.site.register(Cash_Memo_Design_Model)
admin.site.register(save_template_for_cashmemo)
admin.site.register(save_template_for_receipt)
admin.site.register(save_stamp_for_cashmemo)
admin.site.register(save_stamp_for_receipt)
admin.site.register(cash_memo_template_images)

