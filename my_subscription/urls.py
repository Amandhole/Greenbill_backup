from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path("add-contact-us-form/", save_contact_form_subscriptions_requirements, name="add-contact-us-form"),

    path("recharge/", recharge_subscriptions, name="recharge"),

    path("get-subscription-plan-by-id/<int:id>/", get_plan_by_id, name="get-subscription-plan-by-id"),

    path("get-promotional-sms-plan-by-id/<int:id>/", get_promotional_sms_plan_by_id, name="get-promotional-sms-plan-by-id"),

    path("get-transactional-sms-plan-by-id/<int:id>/", get_transactional_sms_plan_by_id, name="get-transactional-sms-plan-by-id"),

    path("get-adon-sms-plan-by-id/<int:id>/", get_adon_sms_plan_by_id, name="get-adon-sms-plan-by-id"),
    
    path("my-subscription/", my_subscription, name="my-subscription"),
 
    path("recharge-history/", my_subscription_history, name="recharge-history"),

    path('delete-recharge-history/<int:id>', delete_merchant_recharge_history,name="delete-recharge-history"),

    path("subscription-purchased-success/", subscription_purchased_success, name="subscription-purchased-success"),
    path("subscription-purchased-fail/", subscription_purchased_fail, name="subscription-purchased-fail"),

    path("promotional-sms-subscription-purchased-success/", promotional_sms_subscription_purchased_success, name="promotional-sms-subscription-purchased-success"),
    path("promotional-sms-subscription-purchased-fail/", promotional_sms_subscription_purchased_fail, name="promotional-sms-subscription-purchased-fail"),

    path("transactional-sms-subscription-purchased-success/", transactional_sms_subscription_purchased_success, name="transactional-sms-subscription-purchased-success"),
    path("transactional-sms-subscription-purchased-fail/", transactional_sms_subscription_purchased_fail, name="transactional-sms-subscription-purchased-fail"),

    path("add-on-subscription-purchased-success/", add_on_subscription_purchased_success, name="add-on-sms-subscription-purchased-success"),
    path("add-on-subscription-purchased-fail/", add_on_subscription_purchased_fail, name="add-on-subscription-purchased-fail"),
    path('my-subscription-bill/<str:id>/',my_subscription_bill,name="my-subscription-bill"),

    path("get-all-amounts-of-adon/", GetAllAmountsAdon, name="get-all-amounts-of-adon"),
]