from django.contrib import admin
from .models import *

class SuggestBrandadmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'brand', 'location')
admin.site.register(SuggestBrand,SuggestBrandadmin)
