"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
urlpatterns = [
    path("", include("owner_bill_design.urls")),
    path('',include('manual_subscription.urls')),
    path('', include('bill_feedback.urls')),
    path('',include('share_web_offer.urls')),
    path('',include("referral_points.urls")),
    path('',include("owner_coupon.urls")),
    path('',include("owner_bill_info.urls")),
    path('',include("merchant_promotion.urls")),
    path('', include('partner_payment.urls')),
    path('', include('partner_my_subscription.urls')),
    path('', include('merchant_payment.urls')),
    path('',include("owner_stamp.urls")),
    path('',include("merchant_stamp.urls")),
    path('',include("offers_status.urls")),
    path('', include("offer_cusavailable.urls")),
    path('', include("partner_merchant_info.urls")),
    path('',include("owner_customer_info.urls")),
    path('', include("feedback.urls")),
    path('', include("suggest_a_brand.urls")),
    path('', include("share_a_word.urls")),
    path('', include("payments.urls")),
    path('', include("suggest.urls")),
    path('', include("userlog.urls")),
    path('', include("merchant_cashmemo_design.urls")),
    path('', include("bill_design.urls")),
    path('', include("system_update.urls")),
    path('', include("supports_faq.urls")),
    path('', include('promotions.urls')),
    path('', include('bill_info.urls')),
    path('', include("merchant_cash_memo.urls")),
    path('', include("offers.urls")),
    path('', include('cash_memo_receipts.urls')),
    path('', include("customer_coupon.urls")),
    path('', include("coupon.urls")),
    path('', include('customer_search.urls')),
    path('', include('owner_notice_board.urls')),
    path('', include('merchant_notice.urls')),
    path('', include('my_subscription.urls')),
    path('', include('parking_lot_apis.urls')),
    path('', include('customer_info.urls')),
    path('', include('green_points.urls')),
    path('', include('shopping_analysis.urls')),
    path('', include('merchant_enquiry.urls')),
    path('', include('customer_bill.urls')),
    path('', include('partner_info.urls')),
    path('', include('petrol_pump_apis.urls')),
    path('', include('backup_restore.urls')),
    path('', include('merchant_software_apis.urls')),
    path('', include('merchant_info.urls')),
    path('', include('customer_apis.urls')),
    path('', include('merchant_apis.urls')),
    path("", include("subscription_plan.urls")),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path("", include("super_admin_settings.urls")),
    path("", include("partner_setting.urls")),
    path("", include("merchant_role.urls")),
    path("", include("merchant_setting.urls")),
    path("", include("category_and_tags.urls")),
    path("", include("software_partner_user.urls")),
    path("", include("dashboard_user.urls")),
    path("", include("role.urls")),
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("users.urls")),
    path("", include("app.urls")),           # UI Kits Html files
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)