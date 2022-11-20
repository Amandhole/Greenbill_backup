from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(StampModel)
admin.site.register(merchantusagestamp)
admin.site.register(merchantstampupload)
admin.site.register(selectstampimage)
admin.site.register(usecashmemostamp)
admin.site.register(usereceiptrstamp)
