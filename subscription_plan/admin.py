from django.contrib import admin

from .models import *

admin.site.register(subscription_plan_details)
admin.site.register(promotional_subscription_plan_model)
admin.site.register(transactional_subscription_plan_model)
admin.site.register(add_on_plan_model)