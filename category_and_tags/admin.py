from django.contrib import admin

# Register your models here.
from .models import business_category, bill_tags, bill_category
# Register your models here.
admin.site.register(business_category)
admin.site.register(bill_tags)
admin.site.register(bill_category)