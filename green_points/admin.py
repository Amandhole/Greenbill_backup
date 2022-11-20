from django.contrib import admin
from .models import *

class GreenPointsAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'green_points_count')
admin.site.register(GreenPointsModel,GreenPointsAdmin)