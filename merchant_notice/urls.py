from django.urls import path
from merchant_notice import views

urlpatterns = [

    path("merchant-notice-board/", views.Merchant_Notice_Board, name="merchant-notice-board"),
    path("merchant-notice-board-list/", views.merchantNoticeBoardList, name="merchant-notice-board-list"),
    path("read-merchant-notification/", views.readMerchantNotification, name="read-merchant-notification"),
    path('delete-merchant-notice/<int:id>',views.deletemerchantnotice,name="delete-merchant-notice"),
]
