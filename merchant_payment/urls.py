from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path("merchant-get-payment-link/", GetPaymentLink, name="merchant-get-payment-link"),
    path('merchant-send-payment-link/<int:id>/', SendPaymentLink, name="merchant-send-payment-link"),
    path('merchant-delete-payment-link/<int:id>/', DeletePaymentLink, name="merchant-delete-payment-link"),
    path('payment-link/<str:id>/', PaymentLink, name="payment-link"),
    path('merchant-payment-link-success/', payment_link_success, name="merchant-payment-link-success"),
    path('merchant-payment-link-fail/', payment_link_fail, name="merchant-payment-link-fail"),
    path('merchant-received-payments/', ReceivedPayments, name="merchant-received-payments"),
    path('merchant-payment-history/', PaymentHistory, name="merchant-payment-history"),

    # UPI Link 

    path("payment-upi/",payment_upi,name="payment-upi"),

]