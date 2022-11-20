from django.contrib import admin
from django.urls import path,include
from .import views
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path("stampview/",views.stampview, name="stampview"), 

    path("save-stamp-image/",views.save_merchant_stampImage, name="save-stamp-image"),
    path("merchant-stamp-select-img/", views.save_image_select, name="merchant-stamp-select-img"),

    path("merchant-stamp-cropped-img-upload/", views.stamp_cropped_image_upload, name="merchant-stamp-cropped-img-upload"),

    path("delete-merchant-own-stamp/<int:id>", views.DeleteMerchantOwnStamp, name="delete-merchant-own-stamp")
]
