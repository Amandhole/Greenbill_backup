from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(merchant_role)

admin.site.register(merchant_module)

admin.site.register(merchant_feature)

admin.site.register(merchant_permission)

admin.site.register(merchant_userrole)