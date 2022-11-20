from django.contrib import admin

from .models import notification_settings, GreenPointsSettings, GreenPointsEarnedHistory

admin.site.register(notification_settings)

admin.site.register(GreenPointsSettings)

admin.site.register(GreenPointsEarnedHistory)