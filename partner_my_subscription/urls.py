from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path("partner-recharge/", recharge_subscriptions, name="partner-recharge"),
    path("partner-my-subscription/", my_subscription, name="partner-my-subscription"),
 
    path("partner-recharge-history/", my_subscription_history, name="partner-recharge-history"),

    path("partner-subscription-purchased-success/", subscription_purchased_success, name="partner-subscription-purchased-success"),
    path("partner-subscription-purchased-fail/", subscription_purchased_fail, name="partner-subscription-purchased-fail"),

    path("partner-promotional-sms-subscription-purchased-success/", promotional_sms_subscription_purchased_success, name="partner-promotional-sms-subscription-purchased-success"),
    path("partner-promotional-sms-subscription-purchased-fail/", promotional_sms_subscription_purchased_fail, name="partner-promotional-sms-subscription-purchased-fail"),

    path("partner-transactional-sms-subscription-purchased-success/", transactional_sms_subscription_purchased_success, name="partner-transactional-sms-subscription-purchased-success"),
    path("partner-transactional-sms-subscription-purchased-fail/", transactional_sms_subscription_purchased_fail, name="partner-transactional-sms-subscription-purchased-fail"),

    path("partner-add-on-subscription-purchased-success/", add_on_subscription_purchased_success, name="partner-add-on-sms-subscription-purchased-success"),
    path("partner-add-on-subscription-purchased-fail/", add_on_subscription_purchased_fail, name="partner-add-on-subscription-purchased-fail"),
    path('my-subscription-bill-partner/<str:id>/',my_subscription_bill,name="my-subscription-bill-partner"),

    path('get-partner-subscription-plan-by-id/<str:id>/',GetPartnerSubscriptionPlanById,name="get-partner-subscription-plan-by-id"),
]