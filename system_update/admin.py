from django.contrib import admin

from .models import *

admin.site.register(system_updates)
admin.site.register(unread_system_updates)