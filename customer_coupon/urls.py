
from django.contrib import admin
from django.urls import path, include
from customer_coupon import views

urlpatterns = [
    path("customer-coupons-redeem/",
         views.views_customer_coupon, name="customer-coupons-redeem"),
    path("coupon-history/",views.Coupon_History,name="coupon-history"),
    path("customer-owner-coupons-redeem/",
         views.views_customer_owner_coupon, name="customer-owner-coupons-redeem"),
    path("owner-coupon-history/",views.Owner_Coupon_History,name="owner-coupon-history"),
    path("view-coupon-record/<int:id>",views.view_coupon_record, name="view-coupon-record"),

    path("save-number-of-visit/", views.Number_of_views, name="save-number-of-visit"),
    

]
