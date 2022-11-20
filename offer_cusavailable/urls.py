from django.contrib import admin
from django.urls import path,include
from .import views


urlpatterns = [
    path("customer-view-offer/",views.availview, name="customer-view-offer"), 
    # path("merchant_general_setting/",views.merchant_general_setting, name="merchant_general_setting"), 
    path("view-offer-record/<int:id>",views.view_offer_record, name="view-offer-record"),
    path("store-number-of-visit/", views.Number_of_views, name="store-number-of-visit"),  
    
     
]