from django.urls import path
from .views import *

urlpatterns = [
    path("system-update-add/", system_update_view, name="system-update-add"),
    path("delete-system-update-by-id/<int:id>", delete_system_update_by_id, name="delete-system-update-by-id"),
    path("get-system-update-details/", get_system_update_by_id, name="get-system-update-details"),
    path("customer-system-updates/", customer_system_updates, name="customer-system-updates"),
    path("merchant-system-updates/", merchant_system_updates, name="merchant-system-updates"),
    path("partner-system-updates/", partner_system_updates, name="partner-system-updates"),
    path("update-system-update-read-status-merchant/", update_system_update_read_status_merchant, name="update-system-update-read-status-merchant"),
    path("update-system-update-read-status-partner/", update_system_update_read_status_partner, name="update-system-update-read-status-partner"),
]