"""
Copyright (c) 2020 - present ZappKode Solutions

"""

from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    # Subscription plans
    path("get-subscription-plans/", get_subscription_plans, name="get-subscription-plans"),
    path("subscription-plans/", subscription_plans, name="subscription-plans"),
    path("get-subscription-plans/<int:id>/", get_subscription_plans_by_id, name="get-subscription-plans-by-id"),
    path("delete-subscription-plans/<int:id>/", delete_subscription_plans, name="delete-subscription-plans"),
    path("enable-subscription-plans/<int:id>/", enable_subscription_plans, name="enable-subscription-plans"),
    path("disable-subscription-plans/<int:id>/", disable_subscription_plans, name="disable-subscription-plans"),
    
    # Promotional Plans
    path("get-promotional-subscription-plan/", Promotions_Subscription_Plan,name="get-promotional-subscription-plan"),
    path("get-promotionals-plans/<int:id>/",Get_Promotional_plan_by_id, name="get-promotionals-plans"),
    path("delete-promotional-plan/<int:id>/", Delete_promotional_plan,name="delete-promotional-plan"),
    path("disable-promotional-plans/<int:id>/",Disable_Promotional_Plan,name="disable-promotional-plans"),
    path("enable-promotional-plans/<int:id>/",Enable_Promotional_Plan,name="enable-promotional-plans"),

    # Transactional Plans
    path("get-transactional-subscription-plan/", transactional_subscription_plan,name="get-transactional-subscription-plan"),
    path("get-transactional-plans/<int:id>/",get_transactional_plan_by_id, name="get-promotionals-plans"),
    path("delete-transactional-plan/<int:id>/", delete_transactional_plan,name="delete-transactional-plan"),
    path("disable-transactional-plans/<int:id>/",disable_transactional_plan,name="disable-transactional-plans"),
    path("enable-transactional-plans/<int:id>/",enable_transactional_plan,name="enable-transactional-plans"),

    # Add On's Plans
    path("get-add-on-plan/", add_on_plan, name="get-add-on-plan"),
    path("get-add-on-plan/<int:id>/", get_add_on_plan_by_id, name="get-add-on-plan-by-id"),
    path("delete-add-on-plan/<int:id>/", delete_add_on_plan, name="delete-add-on-plan"),
    path("disable-add-on-plan/<int:id>/", disable_add_on_plan, name="disable-add-on-plan"),
    path("enable-add-on-plan/<int:id>/", enable_add_on_plan, name="enable-add-on-plan"),

    # Offers Plans
    path("get-offers-subscription-plans/", get_offers_subscription_plans, name="get-offers-subscription-plans"),

    path("view-subscription-plans-details/<subscription_name>/", view_subscription_status, name="view-subscription-plans-details"),
    path("view-subscription-plans-details_transitional/<subscription_name>/", view_subscription_status_Transitional, name="view-subscription-plans-details_transitional"),
    path("view-subscription-plans-details_promotional/<subscription_name>/", view_subscription_status_promotional, name="view-subscription-plans-details_promotional"),

    path("merchant-contact-subscriptions-request/", merchant_contact_for_subscriptions, name="merchant-contact-subscriptions-request"),

    path("delete-subscriptions-request-enquiry/<int:id>", Delete_Enquiry, name="delete-subscriptions-request-enquiry"),

]
