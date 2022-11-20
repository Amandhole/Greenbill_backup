from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('partner-business/', partnerbusiness, name="partner-business"),
    path('delete-partner-business/<int:id>', deletePartnerBusiness, name="delete-partner-business"),
]