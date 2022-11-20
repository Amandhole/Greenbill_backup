# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hind Softwares
"""

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('customer-register/', customer_register_view, name="customer register"),
    path('customer-login/', customer_login_view, name="customer login"),
    path("customer-logout/", customer_logout_view, name="customer logout"),
    path("customer-merchant-switch/", customer_merchant_switch_view, name ="customer merchant switch"),
    path('merchant-register/', merchant_register_view, name="merchant register"),
    path('merchant-login/', merchant_login_view, name="merchant login"),
    path("merchant-logout/", merchant_logout_view, name="merchant logout"),
    path("merchant-customer-switch/", merchant_customer_switch_view, name = "merchant customer switch"),
    # path('partner-register/', software_partner_register_view, name="software partner register"),
    path('partner-login/', software_partner_login_view, name="software partner login"),
    path("partner-logout/", partner_logout_view, name="partner logout"),
    path("generate-otp/", generate_otp, name="generate otp"),
    path("generate-otp-merchant/", generate_otp_merchant, name="generate otp merchant"),
    path("generate-otp-partner/", generate_otp_partner, name="generate otp partner"),
    path("validate-mobile-no/", validate_mobile_no_view, name="validate mobile no"),
    path("validate-register-otp/", register_otp_validation_view, name="validate register otp"),
    path('become-customer/', become_customer, name="become customer"),
    path('become-merchant/', become_merchant, name="become merchant"),
    path("merchant-validate-referral-code/", merchant_validate_referral_code_view, name="merchant-validate-referral-code"),
    path("customer-validate-referral-code/", customer_validate_referral_code_view, name="customer-validate-referral-code"),
    path('email-verification/<str:id>/', email_verification_view, name="email-verification"),
    path("customer-validate-mobile-no/",customer_validate_mobile_no, name="customer-validate-mobile-no"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 