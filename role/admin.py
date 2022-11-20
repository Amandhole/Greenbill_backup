from django.contrib import admin

from .models import role, module, feature, permission, userrole

# Register your models here.

admin.site.register(role)

admin.site.register(module)

admin.site.register(feature)

admin.site.register(permission)

admin.site.register(userrole)