
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('user-logs/', userlogs, name="user-logs"),
    path('merchant-user-logs/<str:mobile_no>/', merchant_userlogs, name="merchant-user-logs"),
    path('merchant-logs-details/', MerchantUserlogsDetails, name="merchant-logs-details"),
    path('merchant-list-for-user-log/',merchant_list_for_userlogs, name="merchant-list-for-user-log"),
    path('owner-logs/<str:mobile_no>/', owner_logs, name="owner-logs"),
]