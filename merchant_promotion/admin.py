from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(bulkMailSmsMerchantCustomerModel)
admin.site.register(smsHeaderModel)
admin.site.register(templateContentModel)