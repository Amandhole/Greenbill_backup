from django.urls import path, re_path, include
from django.conf.urls import url, include
from app import views
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("profile-image-remove/", profile_image_remove, name="profile image remove"),
    path("merchant-profile-image-remove/", merchnat_profile_image_remove, name="merchant profile image remove"),
    path("partner-profile-image-remove/", partner_profile_image_remove, name="partner profile image remove"),
    path("customer-profile-image-remove/", customer_profile_image_remove, name="customer profile image remove"),
    path("merchant-profile/", merchant_profile , name="merchant profile"),
    path("partner-profile/", partner_profile , name="partner profile"),
    path("customer-profile/", customer_profile , name="customer-profile"),
    path("merchant-upload-croped-profile/", upload_crop_merchant_profile_image,name="upload_crop_merchant_profile_image"),
    path("customer-upload-croped-profile/", upload_croped_customer_profile_image,name="customer-upload-croped-profile"),
    path("partner-upload-croped-profile/", upload_crop_partner_profile_image,name="partner-upload-croped-profile"),
    path("owner-upload-crop-image/", upload_crop_profile_image,name="owner-upload-crop-image"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)