from django.contrib import admin
from .models import *

class Feedbackadmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'bug', 'suggestion', 'comments')
admin.site.register(Feedback,Feedbackadmin)
