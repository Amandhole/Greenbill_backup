from django.urls import path
from .views import *

urlpatterns = [
	
	path("owner-received-bills/", owner_received_bills_view, name="owner-received-bills"),
    path("owner-rejected-bills/", owner_rejected_bills_view, name="owner-rejected-bills"),
]