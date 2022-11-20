from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path("wstampview/",views.wstampview, name="wstampview"), 
    path("delete-stamp/<int:id>", views.Delete_Offer, name="delete-stamp"),
    path("stampdview/",views.stampdview, name="stampdview"), 
]