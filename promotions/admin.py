from django.contrib import admin
from .models import *

admin.site.register(ads_for_merchants,)

admin.site.register(bulkMailSmsModel)

admin.site.register(ads_below_bill)


admin.site.register(ads_for_green_bills)