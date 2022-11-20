from django.contrib import admin

from .models import bill_designs, authorised_sign,temp_pdf_check,contact_card,Card_feedback

admin.site.register(bill_designs)
admin.site.register(authorised_sign)

admin.site.register(temp_pdf_check)

admin.site.register(contact_card)

admin.site.register(Card_feedback)