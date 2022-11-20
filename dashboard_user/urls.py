"""
Copyright (c) 2020 - present Hind Softwares

""" 

from django.urls import path, re_path
from .views import register_user_view, update_user_view, delete_user_view, disable_user_view, enable_user_view, all_disable_user, ownerchangeuserpassword
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-admin-panel-user/', register_user_view, name="create-admin-panel-user"),
    path('update-admin-panel-user/', update_user_view, name="update-admin-panel-user"),
    path('delete-admin-panel-user/<int:id>', delete_user_view, name="delete-admin-panel-user"),
    path('disable-admin-panel-user/<int:id>', disable_user_view, name="disable-admin-panel-user"),
    path('enable-admin-panel-user/<int:id>', enable_user_view, name="enable-admin-panel-user"),
    path('admin-disable-paner-user/', all_disable_user, name="admin-disable-paner-user"),
    path('owner-change-user-password/', ownerchangeuserpassword, name="owner-change-user-password"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)