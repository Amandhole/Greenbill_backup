from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path("customer_list/",views.owner_customer_info,name="customer_list"),
    # path("delete-customer/<int:id>", views.Delete_customer, name="delete-customer"), 
    path("delete-customer-list/<int:id>", views.Delete_customer, name="delete-customer-list"),
    path("customer_list/<str:contact_no>", views.customer_data_by_mobile_no, name="customer_data_by_mobile_no"),
    path("edit_customer_info/", views.Edit_Customer_info, name="edit_customer_info"),
    path("customer-info-send-bill-sms-web-owner/<int:id>/", views.CustomerInfoSendBillSMSWeb, name="customer-info-send-bill-sms-web-owner"),
    
    path("views-cashmemo-by-no/<str:contact_no>/", views.ViewAllCashMemoByNumber, name="views-cashmemo-by-no"),

    path("views-receipt-by-no/<str:contact_no>/", views.ViewAllReceiptMemoByNumber, name="views-receipt-by-no"),
]