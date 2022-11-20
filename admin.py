from django.contrib import admin
from .models import *

admin.site.register(merchant_subscriptions)
admin.site.register(recharge_history)
admin.site.register(promotional_sms_subscriptions)
admin.site.register(transactional_sms_subscriptions)
admin.site.register(sent_bill_history)
admin.site.register(contact_for_subscriptions_requirements)