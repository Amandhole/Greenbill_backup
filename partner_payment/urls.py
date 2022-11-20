from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path("partner-get-payment-link/", GetPaymentLink, name="partner-get-payment-link"),
    path('partner-send-payment-link/<int:id>/', SendPaymentLink, name="partner-send-payment-link"),
    path('partner-delete-payment-link/<int:id>/', DeletePaymentLink, name="partner-delete-payment-link"),
    path('partner-payment-link/<str:id>/', PaymentLink, name="partner-payment-link"),
    path('partner-payment-link-success/', payment_link_success, name="partner-payment-link-success"),
    path('partner-payment-link-fail/', payment_link_fail, name="partner-payment-link-fail"),
    path('partner-received-payments/', ReceivedPayments, name="partner-received-payments"),
    path('partner-payment-history/', PaymentHistory, name="partner-payment-history"),
]