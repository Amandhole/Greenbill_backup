"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [

    # Email Templates
    path("email-templates/", email_templates, name="email-templates"),

    # Notification Settings
    path("notification-settings/", notification_settings_view, name="notification-settings"),
    path("notification-settings/<int:id>/", get_notification_settings_by_id, name="get-notification-settings-by-id"),
    path('notification-settings/message-update/<int:id>/', notification_message_update_view, name="notification-message-update"),
    path("payment-setting/", payment_setting, name="payment-setting"),
    path('sms-setting/', smsSetting, name="sms-setting"),
    path("green-point-settings/", green_point_settings, name="green-point-settings"),
    path("manage-companies-dmr/", manage_comapanies_dmr, name="manage-companies-dmr"),
    path("delete-companies-dmr/<int:id>",deletecompaniesdmr, name="delete-companies-dmr"),
]