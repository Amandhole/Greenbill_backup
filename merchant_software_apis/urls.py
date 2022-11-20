from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('send-bill/', send_bill, name="send-bill"), 
    path('send-bill-sms-api/', send_bill_sms, name="send-bill-sms-api/"),
    path('send-bill-email-api/', send_bill_email, name="send-bill-email-api/"),
    path('send-bill-sms-and-email-api/', send_bill_sms_and_email, name="send-bill-sms-and-email-api/"),
    path('store-device-id-api/', storeDeviceId, name="store-device-id-api"),
    path('destroy-device-id-api/', destroyDeviceId, name="destroy-device-id-api"),
    path('send-bill-website-api/', send_bill_website, name="send-bill-website-api"),
    path('demo-bill/', website_demo_bill, name="demo-bill"),
    path('get-is-merchant-or-customer-sw/', get_is_merchant_or_customer, name="get-is-merchant-or-customer-sw"),
    path('get-merchant-business-sw/', get_merchant_business, name="get-merchant-business-sw"),
    
    path('my-bill-merchant/<str:id>/', my_bill_merchant, name="my-bill-merchant"),

    path('search-show-bill/<str:id>/', search_view_bill, name="search-show-bill"),

    path('exe-print-status/', exe_print_record_maintain, name="exe-print-status"),

    #habrone bill 
    path('my-green-bill/<str:id>/', my_green_bill, name="my-green-bill"),

    # Update Rating
    path('update-customer-bill-rating/<str:id>/', update_customer_bill_rating, name="update-customer-bill-rating"),
    path('update-merchant-bill-rating/<str:id>/', update_merchant_bill_rating, name="update-merchant-bill-rating"),

    # Reject Bill
    path('merchant-reject-bill/', reject_merchant_bill, name="merchant-reject-bill"),
    path('customer-reject-bill/', reject_customer_bill, name="customer-reject-bill"),

    # Update Feedback
    path("customer-update-bill-feedback/", customer_update_bill_feedback, name="customer-update-bill-feedback"),
    path("merchant-update-bill-feedback/", merchant_update_bill_feedback, name="merchant-update-bill-feedback"),
    
    path('software-login-api/', merchantsoftwarelogin, name="software-login-api"),
    path('check-subscription-available-sw-api/', check_subscription_available, name="check-subscription-available-sw-api"),
    path('my-bill-merchant-payment-link-success/',payment_link_success,name="my-bill-merchant-payment-link-success"),
    path('my-bill-merchant-payment-link-fail/',payment_link_fail,name="my-bill-merchant-payment-link-fail"),
    path("view-merchant-ads-url/<str:id>/", view_merchant_ads, name="view-merchant-ads-url"),

    path('get-merchant-business-names-api/', getMerchantBusinesses, name="get-merchant-businesses-api"),
    # path('get-merchant-stamp-api/', getMerchantStamp, name="get-merchant-stamp-api"),
    path('get-stamp-names-api/',getStampNames, name="get-stamp-names-api"),

    path('fetch-amount-from-image/',FetchAmountFromImage, name="fetch-amount-from-image"),

    path('fetch-invoice-number-from-image/',FetchInvoiceNumberFromImage, name="fetch-invoice-number-from-image"),

    path('get-sample-bill-api/',get_sample_bill, name="get-sample-bill-api"),

    path('ciferon-send-bill-api/',CiferonSendBill, name="ciferon-send-bill-api"),

    path('habron-send-bill-api/',HabronSendBill, name="hebrone-send-bill-api"),

    path('testing-hebrone-send-bill-api/',testingHebroneSendBill, name="hebrone-send-bill-api"),

    path('green-bill-send-bill-api/',GreenBillSendBillApi, name="green-bill-send-bill-api"),

    path('green-bill-common-send-bill1-api/',GreenBillCommonSendBillApi1, name="green-bill-common-send-bill1-api"),

    path('send-bill2-green-bill-api/',CommonSendBillGreenBillApi2, name="send-bill2-green-bill-api"),

    path('green-bill-common3-api/',GreenBillCommon3Api, name="green-bill-common3-api"),

    # path('check-subscription-availability-status/',check_status_subscription_availlabilty, name="check-subscription-availability-status"),

    path('get-green-bill-merchant-business-id-by-number/',GetMerchantBusinessIdsByNumber, name="get-green-bill-merchant-business-id-by-number")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
