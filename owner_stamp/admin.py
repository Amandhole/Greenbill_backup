from django.contrib import admin

from .models import wstampmodels, stampdmodels
# Register your models here.
admin.site.register(wstampmodels)
admin.site.register(stampdmodels)

