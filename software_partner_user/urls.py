"""
Copyright (c) 2020 - present Hind Softwares

""" 

from django.urls import path, re_path
from .views import register_software_partner_view, update_software_partner_view, delete_software_partner_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-software-partner/', register_software_partner_view, name="create-software-partner"),
    path('update-software-partner/', update_software_partner_view, name="update-software-partner"),
    path('delete-software-partner/<int:id>', delete_software_partner_view, name="delete-software-partner")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)