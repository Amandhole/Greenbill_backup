from django.urls import path
from .views import *


urlpatterns = [

    path("owner-notice-board/", ownerNoticeBoard, name="owner-notice-board"),
    path("get-individual-by-category/",get_individual_by_category, name="get-individual-by-category"),
    path("owner-notice-board-list/", ownerNoticeBoardList, name="owner-notice-board-list"),
    path("read-owner-notification/", readOwnerNotification, name="read-owner-notification"),
    # path('owner-merchant-notice-board/', ownerMerchantNoticeBoard, name="owner-merchant-notice-board"),
    path('owner-merchant-notice-board-list/', ownerMerchantNoticeBoardList, name="owner-merchant-notice-board-list"),
    # path('owner-partner-notice-board/', ownerPartnerNoticeBoard, name="owner-partner-notice-board"),
    path('owner-partner-notice-board-list/', ownerPartnerNoticeBoardList, name="owner-partner-notice-board-list"),
    # path('owner-customer-notice-board/', ownerCustomerNoticeBoard,name="owner-customer-notice-board"),
    path('customer-notice-board-list/',ownerCustomerNoticeBoardList , name="owner-customer-notice-board-list"),
    path('delete-owner-notice/<int:id>',deleteownernotice,name="delete-owner-notice"),
    path('delete-merchant-owner-notice/<int:id>',deletemerchantownernotice,name="delete-merchant-owner-notice"),

    path('delete-owner-notice-board-messages/<int:id>',DeleteOwnerNoticeBoardMessages,name="delete-owner-notice-board-messages"),

    path("save-owner-notice-board-message/", saveOwnerMessages, name="save-owner-notice-board-message"),
]