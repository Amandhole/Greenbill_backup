
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("view-merchant-cash-memo/", views.view_all_cash_memo,
         name="view-merchant-cash-memo")
]
