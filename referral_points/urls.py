from django.contrib import admin
from django.urls import path,include
from .import views 

urlpatterns = [
    path("referral-points/",views.Get_Referral_points,name="referral-points"), 

    path("add-promotions-amount/",views.add_promotions_amount,name="add-promotions-amount"), 

]