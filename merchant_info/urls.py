from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    #path("add/", views.merchant_add, name="merchant_add"),
    #path('<int:id>/', views.merchant_add, name='merchant_update'),
    path("merchant-info/", merchant_info, name="merchant-info"),
    path("change-active-merchant-status/", changeStatus, name="change-active-merchant-status"),

    path("add-merchant-by-admin/", addMerchantByAdmin, name="add-merchant-by-admin"),
    path("merchant-info-view/<int:id>/", viewMerchantInfo, name="merchant-info-view"),
    path("get-merchant-business-details/", getMerchantBusinessDetails , name="get-merchant-business-details"),
    path("edit-merchant-business-info/", editMerchantBusinessInfo, name="edit-merchant-business-info"),
    path("disable-merchant-from-admin/", disableMerchantFromAdmin, name="disable-merchant-from-admin"),
    path("enable-merchant-from-admin/<int:id>", enableMerchantFromAdmin, name="enable-merchant-from-admin"),
    path("merchant-by-sales/", merchantBySales, name="merchant-by-sales/"),
    path('disapprove-merchant/',disapproveMerchant, name="disapprove-merchant"),
    path("list/edit/<int:id>/", merchant_edit, name="merchant_edit"),
    path('list/delete/<int:id>/', merchant_delete, name="merchant_delete"),
    path('merchant-business/', merchantBusinesses, name="merchant-business"),
    path('delete-merchant-business/<int:id>', deleteMerchantBusiness, name="delete-merchant-business"),
    path("edit_my_bussiness/", EditMyBussiness, name="edit_my_bussiness"),
    path('delete-merchant-business-owner/<int:id>', deleteMerchantBusinessOwner, name="delete-merchant-business-owner"),


    path("delete_disabled_merchant/<int:id>", Delete_Disabled_Merchant, name="delete_disabled_merchant"),
    path("merchant-disabled/",disabledMerchant, name="merchant-disabled" ),
    path("merchant-latest/", latestMerchant, name="merchant-latest"),
    path('merchant-business-branch/', merchantBusinessesBranch, name="merchant-business-branch"),
    path('send-merchant-notice/',sendMechantNotice,name="send-merchant-notice"),
    path('disable-merchant-reason/', disabledMerchantReason, name="disable-merchant-reason"),
    path('delete-reason/<int:id>' , Delete_Reason, name="delete-reason"),
    path('merchant-detail-view/<int:id>/', merchantDetailView, name="merchant-detail-view"),

    path('view-merchant-offer-details/<int:id>/', ViewMerchantOffers, name="view-merchant-offer-details"),

    path('view-merchant-coupon-list-details/<int:id>/', ViewMerchant_couponList, name="view-merchant-coupon-list-details"),

    path("view-all-merchant-info-record/<int:id>/", view_all_Merchant_Details, name="view-all-merchant-info-record"),

    path("edit-merchant-data/", Edit_all_merchant_information, name="edit-merchant-data"),


]