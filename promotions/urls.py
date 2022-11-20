from django.urls import path
from .views import *


from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("ads-below-bills/", ads_below_bills, name="ads-below-bills"),
    path("edit-ads-below-bill/", edit_ads_by_id, name="edit-ads-below-bill"),
    path("get-ads-details/", get_ads_details_by_id, name="get-ads-details"),
    path("delete-ads-by-id/<int:id>", delete_ads_by_id, name="delete-ads-by-id"),
    path("get-all-ads-below-bill/", get_all_ads_below_bill, name="get-all-ads-below-bill"),
    path("approve-ads-by-id/<int:id>", approve_ads_by_id, name="approve-ads-by-id"),
    path("disapprove-ads-by-id/", disapprove_ads_by_id, name="disapprove-ads-by-id"),
    path("set-active-ads/", set_active_ads, name="set-active-ads"),
    
    path("ads-for-merchants/", ads_for_merchant, name="ads-for-merchants"),
    
    path("add-payment-for-third-party-ads/", add_payment_for_third_party_ads, name="add-payment-for-third-party-ads"),

    path("get-merchant-ads-details/", get_merchant_ads_details_by_id, name="get-merchant-ads-details"),
    path("edit-merchant-ads-below-bill/", edit_merchant_ads_by_id, name="edit-merchant-ads-below-bill"),
    path("delete-merchant-ads-by-id/<int:id>", delete_merchant_ads_by_id, name="delete-merchant-ads-by-id"),
    path("set-merchant-active-ads/", set_merchant_active_ads, name="set-merchant-active-ads"),
    path("ads-for-green-bill/", ads_for_green_bill, name="ads-for-green-bill"),
    path("get-green-bill-ads-details/", get_green_bill_ads_details_by_id, name="get-green-bill-ads-details"),
    path("edit-green-bill-ads-below-bill/", edit_green_bill_ads_by_id, name="edit-green-bill-ads-below-bill"),
    path("delete-green-bill-ads-by-id/<int:id>", delete_green_bill_ads_by_id, name="delete-green-bill-ads-by-id"),
    path("set-green-bill-active-ads/", set_green_bill_active_ads, name="set-green-bill-active-ads"),
    path("deactive-ads-by-id/<int:id>", deactive_ads_by_id, name="deactive-ads-by-id"),
    path('bulk-sms/',bulkSms,name="bulk-sms"),
    path('bulk-mail/',bulkMail,name="bulk-mail"),
    path('delete-bulk-mail/<int:id>',deleteBulkmail,name="delete-bulk-mail"),
    path('delete-bulk-sms/<int:id>',deleteBulksms,name='delete-bulk-sms'),
    path('scheduled-bulk-mail-sms/',scheduleBulkMailSms,name="scheduled-bulk-mail-sms"),
    path('category-count/',categorycount,name="category-count"),
    path("approve-thir-party-ads-by-id/<int:id>", approve_third_party_ads_by_id, name="approve-thir-party-ads-by-id"),
    path("approve-third-party-ads/<int:id>", approve_third_party_ads, name="approve-third-party-ads"),
    path("disapprove-third-party-ads-by-id/", disapprove_third_party_ads_by_id, name="disapprove-third-party-ads-by-id"),
    # path("delete-green-bill-ads-by-id/<int:id>", delete_green_bill_ads_by_id, name="delete-green-bill-ads-by-id"),

    path("add-third-party-amount-by-id/", add_third_party_amount_by_id, name="add-third-party-amount-by-id"),

    path("active-green-bill-ads/<int:id>", ActiveGreenBillAds, name="active-green-bill-ads"),

    path("delete-green-bill-ads/<int:id>", DeleteGreenBillAds, name="delete-green-bill-ads"),

    path("third-party-purchased-success/", third_party_ads_payment_success, name="third-party-purchased-success"),
    path("third-party-purchased-fail/", third_party_ads_payment_fail, name="third-party-purchased-fail"),

    path("store-ads-clicks/", StoreAds_clicks, name="store-ads-clicks"),


    # path('search-individual', csrf_exempt(search_individual), name="search-individual")
]