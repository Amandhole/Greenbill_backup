from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path("manual-subscription-recharge/", recharge_manual_subscriptions, name="manual-subscription-recharge"),

    path("manual-partner-subscription-recharge/", Partner_recharge_manual_subscriptions, name="manual-partner-subscription-recharge"),
    
    path("get-merchant-by-plan-id/", get_merchants_by_plan_id, name="get-merchant-by-plan-id"),
    
    path("get-merchant-by-promotional-plan-id/", get_merchants_by_promotional_plan_id, name="get-merchant-by-promotional-plan-id"),


    path("manual-subscription-purchased-success/", manual_subscription_purchased_success, name="manual-subscription-purchased-success"),
    path("manual-promotional-sms-subscription-purchased-success/", manual_promotional_sms_subscription_purchased_success, name="manual-promotional-sms-subscription-purchased-success"),
        
    path("manual-transactional-sms-subscription-purchased-success/", manual_transactional_sms_subscription_purchased_success, name="manual-transactional-sms-subscription-purchased-success"),
        
    path("manual-add-on-subscription-purchased-success/", manual_add_on_subscription_purchased_success, name="manual-add-on-sms-subscription-purchased-success"),

    path("get_merchant_gst_address/", GetMerchantAdressForGst, name="get_merchant_gst_address"),

    path("manual-partner-promotional-sms-subscription-purchased-success/", manual_partnerpromotional_sms_subscription_purchased_success, name="manual-partner-promotional-sms-subscription-purchased-success"),

    path("manual-partner-transactional-sms-subscription-purchased-success/", manual_partner_Transactional_sms_subscription_purchased_success, name="manual-partner-transactional-sms-subscription-purchased-success"),

    path("manual-partner-subscription-purchased-success/", manual_partner_GreenBill_subscription_purchased_success, name="manual-partner-subscription-purchased-success"),

    path("manual-partner-adon-purchased-success/", manual_partner_Adon_purchased_success, name="manual-partner-adon-purchased-success"),
        
    ]