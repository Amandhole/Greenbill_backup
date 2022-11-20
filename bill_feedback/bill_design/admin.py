from django.contrib import admin

from .models import bill_designs, authorised_sign

admin.site.register(bill_designs)
admin.site.register(authorised_sign)
