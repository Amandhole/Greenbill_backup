
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path("coupon1/",views.home,name="home"),
    path("coupon/", views.add_coupon_view, name="coupon"),
    path("delete-coupon-by-id/<int:id>", views.Delete_Coupon_by_id, name="delete-coupon-by-id"),
    path("coupon-list/",views.coupon_list, name="coupon-list"),
    path("get-city-by-state-ids-in-coupon/",views.get_city_by_state_ids, name="get-city-by-state-ids-in-coupon"),
    path("get-area-by-city-names-in-coupon/",views.get_area_by_city_names_in_coupon, name="get-area-by-city-names-in-coupon"),

    path("abcd/",views.get_number_of_users_per_coupon, name="abcd"),

    path("get-users-by-state/",views.get_number_of_users_by_sutomer, name="get-users-by-state"),
    path("get-amount-by-state-in-coupon/",views.get_cost_by_cutomer_state, name="get-amount-by-state-in-coupon"),

    path("total-cost-by-users-in-coupon/",views.get_total_cost_per_user, name="total-cost-by-users-in-coupon"),

]
