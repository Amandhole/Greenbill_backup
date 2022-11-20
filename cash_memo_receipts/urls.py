from django.urls import path
from core import settings
from django.conf.urls.static import static
from cash_memo_receipts import views

urlpatterns = [
    path("cash-memo/", views.Cash_memos, name="cash-memo"),
    path("delete-cash-memo/<int:id>",
         views.Delete_Cash_Memo, name="delete-cash-memo"),
    path("edit-cash-memo/", views.Edit_Cash_Memo, name="edit-cash-memo"),
    path("create-receipts/", views.Create_Receipts, name="create-reciepts"),
    path("get-all-merchant-memo-design/", views.All_Cash_Memo_Design,
         name="get-all-merchant-memo-design"),
    path("edit-receipts/", views.Edit_Receipts, name="edit-receipts"),
    path("delete-receipts/<int:id>", views.Delete_Receipts, name="delete-receipts"),
    path('sms-header-request/',views.smsHeaderrequest, name="sms-header-request"),
    path('sms-template-request/',views.smsTemplaterequest, name="sms-template-request"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
