from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    path("payments/", payments, name="payments"),
    path("owner-get-payment-link/", GetPaymentLink, name="owner-get-payment-link"),
    path('owner-send-payment-link/<int:id>/', SendPaymentLink, name="partner-send-payment-link"),
    path('owner-delete-payment-link/<int:id>/', DeletePaymentLink, name="partner-delete-payment-link"),
    path('owner-payment-link/<str:id>/', PaymentLink, name="owner-payment-link"),
    path('owner-payment-link-success/', payment_link_success, name="owner-payment-link-success"),
    path('owner-payment-link-fail/', payment_link_fail, name="owner-payment-link-fail"),
    path('owner-received-payments/', ReceivedPayments, name="owner-received-payments"),

    path('send-payment-manually/', SendPaymentToMerchantAndPartnerManually, name="send-payment-manually"),
#     path('owner-payment-history/', PaymentHistory, name="owner-payment-history"),
 ]