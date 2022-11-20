# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [

    path("test-sms/", test_sms, name="test-sms"),

    path('', include('django.contrib.auth.urls')),
    path("password-reset/", password_reset_request, name="password-reset"),
    path("password-reset-merchant/", password_reset_request_merchant, name="password-reset-merchant"),
    path("password-reset-customer/", password_reset_request_customer, name="password-reset-customer"),
    path("password-reset-partner/", password_reset_request_partner, name="password-reset-partner"),
    path("generate-otp-password/", generate_otp_password, name="generate-otp-password"),
    path("generate-otp-password-merchant/", generate_otp_password_merchant, name="generate-otp-password-merchant"),
    path("generate-otp-password-customer/", generate_otp_password_customer, name="generate-otp-password-customer"),
    path("generate-otp-password-partner/", generate_otp_password_partner, name="generate-otp-password-partner"),


    path("otp-validation-password/", otp_validation_password, name="otp-validation-password"),
    path("password-change-success/", password_change_success, name="password-change-success"),
    
    path('change_password/', change_password_view, name="change password"),

    path("email-setting/", email_setting, name="email-setting"),
    path("general-setting/", general_setting, name="general-setting"),
    
    # The home page
    path('', index, name='home'),
    path('index12/', index12, name='index12'),

    path('merchant-index/', merchant_index, name='merchant home'),
    path('merchant-index1/', merchant_index1, name='merchant home'),

    path("merchant-search/",merchant_search, name="merchant-search"),

    # path('merchant-index1/', merchant_index1, name='merchant home1'),
    path('customer-index/', customer_index, name='customer-home'),
    
    path('partner-index/', partner_index, name='partner home'),

    path('chanage-merchnat-business-view/', chanage_merchnat_business_view, name='chanage merchnat business'),
    path('chanage-merchnat-branch-view/', chanage_merchnat_branch_view, name='chanage merchnat branch'),

    path("owner-business-logo-remove/", owner_business_logo_remove, name="owner-business-logo-remove"),
    path("owner-business-stamp-remove/", owner_business_stamp_remove, name="owner-business-stamp-remove"),
    path("owner-digital-signature-remove/", owner_digital_signature_remove, name="owner-digital-signature-remove"),


    #cropped logo/stamp/signature

    path("owner-upload-signature/", upload_signature_img,name="owner-upload-signature"),
    path("owner-upload-stamp/", upload_stamp_img, name="owner-upload-stamp"),
    path("owner-upload-logo/", upload_logo_img, name="owner-upload-logo"),

    path('customer-index-add-bill/', customer_index_add_bill, name='customer-index-add-bill'),

    #customer parking lot pass
    path("customer-passes/",Parking_Lot_Passes, name="customer-passes"),

    path('customer-payment-history/',customerPaymentHistory, name="customer-payment-history"),

    path('search/', search, name="search"),
    path("download-app/",Download_customer_app, name="download-app"),

    path("test_sms/",test_sms, name="test_sms"),

    #path("merchant-passes/",Merchant_Parking_Lot_Passes,name="merchant-passes"),

    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),

    


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
