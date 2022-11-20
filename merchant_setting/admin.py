from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(MerchantPetrolPump,)
admin.site.register(MerchantParkingAddVehicle,)
admin.site.register(MerchantParkingLotSpace,)
admin.site.register(MerchantParkingSpaceCharges,)
admin.site.register(AddonPetrolPump,)
admin.site.register(parking_app_setting_model,)
admin.site.register(petrol_pump_app_setting_model,)
admin.site.register(MerchantParkingLotPassCharges,)
admin.site.register(flagbillreason)
admin.site.register(CompniesName)
admin.site.register(MerchantPaymentSetting)
admin.site.register(Deleted_Bills_By_Days_setting)  
