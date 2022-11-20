
from django.contrib import admin
from django.urls import path,include
from .views import add_coupon_owner_view, Delete_Coupon, get_city_by_state_ids_in_owner, get_area_by_city_names_in_owner_coupon

urlpatterns = [
    path("owner-coupon/",add_coupon_owner_view,name="owner-coupon"),
    path("delete-coupon/<int:id>", Delete_Coupon, name="delete-coupon"),
    path("get-city-by-state-ids-in-owner-coupon/", get_city_by_state_ids_in_owner, name="get-city-by-state-ids-in-owner-coupon"),
    path("get-area-by-city-names-in-owner-coupon/", get_area_by_city_names_in_owner_coupon, name="get-area-by-city-names-in-owner-coupon"),
]
