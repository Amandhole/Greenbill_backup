from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    # General Setting
    path("partner-general-setting/", partner_general_setting, name="partner-general-setting"),
    path('partner-delete-sms-header/<int:id>', deletepartnerSmsHeader, name="partner-delete-sms-header"),
    path('partner-delete-sms-template/<int:id>', deleteSmstemplatebypartner, name="partner-delete-sms-template"),
    path('active-partner-sms-header-status/<int:id>', activepartnersmsheader, name="active-partner-sms-header-status"),
    path("partner-payment-settings/", partner_payment_setting, name="partner-payment-settings"),
    path('partner-sms-setting/', partnerSmsSetting, name="partner-sms-setting"),
    path("partner-business-logo-remove/", partner_business_logo_remove, name="partner-business-logo-remove"),
    path("partner-business-stamp-remove/", partner_business_stamp_remove, name="partner-business-stamp-remove"),
    path("partner-digital-signature-remove/", partner_digital_signature_remove, name="partner-digital-signature-remove"),


    path('change-partner-inactive-sms-header-status/<int:id>', changeSmsHeaderStatusDisable,name="change-active-sms-header-status"),
    path('change-partner-active-sms-header-status/<int:id>', changeSmsHeaderStatusEnable,name="change-active-sms-header-status"),
    path('delete-partner-sms-header/<int:id>', deleteSmsHeader, name="delete-sms-header"),

    # upload cropped logo/signature/stamp
    path("partner-cropped-logo-upload/", partner_cropped_logo_upload,name="partner-cropped-logo-upload"),
    path("partner-cropped-stamp-upload/", partner_cropped_stamp_upload,name="partner-cropped-stamp-upload"),
    path("partner-cropped-signature-upload/", partner_cropped_signature_upload,name="partner-cropped-signature-upload"),
]