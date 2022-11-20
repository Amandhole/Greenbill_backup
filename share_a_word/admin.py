from django.contrib import admin
from .models import *

class ShareWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'words')
admin.site.register(ShareWord,ShareWordAdmin)
