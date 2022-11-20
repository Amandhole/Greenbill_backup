from django.urls import path
from .views import *

urlpatterns = [
    path("bill-info/", bill_info_view, name="bill-info"),
    path("bill-info-send-bill-sms-web/<int:id>/", BillInfoSendBillSMSWeb, name="bill-info-send-bill-sms-web"),

    path("received-bills/", received_bills_view, name="received-bills"),

    path("rejected-bills/", rejected_bills_view, name="rejected-bills"),
    path("delete-rejected-bill/<int:id>/", delete_rejected_bill_view, name="delete-rejected-bill"),
    path("delete-selected-rejected-bills/", delete_selected_rejected_bills_view, name="delete-selected-rejected-bills"),

    path("send-bill-to-merchant/", send_bill_to_merchant, name="send-bill-to-merchant"),

    path("deletesentbill/<str:id>/<str:db_table>/",delete_sentbill,name="deletesentbill"),
    path("owner-sent-bills/", owner_sent_bills_view, name="owner-sent-bill"),

    path("owner-category-wise-bills/", owner_category_bills_view, name="owner-category-wise-bills"),
    
]