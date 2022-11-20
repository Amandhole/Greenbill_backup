from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path("cashmemo-design/", views.Cash_Memo_Design_View, name="cashmemo-design"),
    path("delete-memo-design/<int:id>", views.Delete_Memo_Design, name="delete-memo-design"),
    path("view-merchant-cash-memo/", views.view_all_cash_memo, name="view-merchant-cash-memo"),
    path("view-merchant-receipts/", views.view_all_receipts, name="view-merchant-receipts"),
    path("delete-cash-memo/<int:id>", views.delete_cash_memo, name="delete-cash-memo"),
    path("delete-receipt/<int:id>", views.delete_receipt, name="delete-receipt"),
    path("receipt-send-web-sms/<int:id>/", views.ReceiptSendWebSms, name="receipt-send-web-sms"),
    path("cash-memo-send-web-sms/<int:id>/", views.CashMemoSendMemoSMSWeb, name="cash-memo-send-web-sms"),
    
# for sample bill 
    

    path("receipt/<str:id>/", views.receipt, name="receipt"),
    
    path('cash-memo/<str:id>/', views.cash_memo, name="cash-memo"),
    path("view-ads-record-cashmemo/<str:id>/", views.view_ads_record_cashmemo, name="view-ads-record-cashmemo"),
    path('save-cash-memo-template/', views.save_cash_memo_template, name="save-cash-memo-template"),
    path('save-receipt-template/', views.save_receipt_template, name="save-receipt-template"),

    path('save-stamp-for-cash-memo/', views.stamp_for_cash_memo, name="save-stamp-for-cash-memo"),

    path('save-stamp-for-receipt/', views.stamp_for_receipt, name="save-stamp-for-receipt"),

    path('unselect-stamp/', views.UnselectCashMemoStamp, name="unselect-stamp"),

    path('unselectreceipt-stamp/', views.unselectreceiptstamp, name="unselectrec,eipt-stamp"),

    path('use-stamp-image/', views.saved_cashmemo_stamp_by_id, name="use-stamp-image"),

    path('unuse-stamp-image/', views.uncheck_cashmemo_stamp_by_id, name="unuse-stamp-image"),

    # path('unuse-stamp-image1/', views.uncheck_cashmemo_stamp_by_id1, name="unuse-stamp-image"),

    path('saved-receipt-stamp-by-id/', views.saved_receipt_stamp_by_id, name="saved-receipt-stamp-by-id"),

    path('uncheck-receipt-stamp-by-id/', views.uncheck_receipt_stamp_by_id, name="uncheck-receipt-stamp-by-id"),

    path('reject-cash-memo-bill/', views.RejectCashMemoBill, name="reject-cash-memo-bill"),

    path('reject-receipt-bill/', views.RejectReceiptBill, name="reject-receipt-bill"),

    path('view-customer-cash-memo/', views.ViewCustomerCashMemo, name="view-customer-cash-memo"),

    path('view-customer-receipts/', views.ViewCustomerReceipts, name="view-customer-receipts"),

    path('save-and-update-cash-memo-template/', views.SaveAndUpdateCashMemoTemplate, name="save-and-update-cash-memo-template"),

    path('save-and-update-receipt-template/', views.SaveAndUpdateReceiptTemplate, name="save-and-update-receipt-template"),

    path('cash-memo-receipt-setting/', views.CashMemoReceiptSettings, name="cash-memo-receipt-setting")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
