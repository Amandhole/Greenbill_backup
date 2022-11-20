from django.contrib import admin

from .models import *

admin.site.register(partner_subscriptions)
admin.site.register(partner_promotional_sms_subscriptions)
admin.site.register(partner_transactional_sms_subscriptions)
admin.site.register(partner_recharge_history)