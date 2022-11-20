from django.urls import path
from customer_bill import views
from core import settings
from django.conf.urls.static import static

urlpatterns = [
    path("customer-bill/", views.Customer_Bill, name="custome_bill"),
    path("edit-customer-bill/", views.Edit_Customer_Bill, name="edit-customer-bill"),
    path("delete-customer-bill/<int:id>/", views.delete_customer_bill, name="delete-customer-bill"),

    # path("my-bills/", views.my_bills, name="my-bills"),
    # path("send-bill-customer/", views.send_bill_customer, name="send-bill-customer"),

    path("my-bills/<str:bill_type>/", views.my_bills, name="my-bills"),
    
    # path("my-bills/", views.my_bills_req, name="my-bills"),

    path("edit-my-bills/", views.Edit_My_Bills, name="edit-my-bills"),
    path("delete-my-bills/<int:id>/", views.Delete_My_Bills, name="delete-my-bills"),
    path("delete-merchant-bills/<int:id>/", views.Delete_merchant_bills,name="delete-merchant-bills"),

    path('my-bill/<str:id>/', views.my_bill, name="my-bill"),
    path('my-bill1/<str:id>/', views.my_bill1, name="my-bill1"),
    path('my-bill2/<str:id>/', views.my_bill2, name="my-bill2"),

    path("new-bill-design/", views.new_bill_design, name="new-bill-design"),

    path("self-added-bill/<str:id>/", views.self_added_bill_view, name="self-added-bill"),

    # path('bills-by-category1/', views.bills_by_bill_category, name="bills-by-category1"),
    # path("edit-bills-by-bill-category/", views.Edit_bills_by_bill_category, name="edit-bills-by-bill-category"),

    # path('bills-by-merchant/', views.bills_by_merchant, name="bills-by-merchant"),
    # path("edit-bills-by-merchant/", views.Edit_bills_by_merchant, name="edit-bills-by-merchant"),
    path('my-bill-payment-link-success/',views.payment_link_success,name="my-bill-payment-link-success"),
    path('my-bill-payment-link-fail/',views.payment_link_fail,name="my-bill-payment-link-fail"),
    path("view-ads-record/<str:id>/", views.view_ads_record, name="view-ads-record"),

    path('get-merchant-business-by-category-id/<int:id>/', views.get_merchant_business_by_category_id, name="get-merchant-business-by-category-id"),

    path('get-image-data/<str:id>/', views.GetImageData, name="get-image-data"),
    
    path('sample-bill-dummy/', views.sample_dummy_bill, name="sample-bill-dummy"),

    path("get-businesses-for-transfer/", views.GetMerchantBillTransfer, name="get-businesses-for-transfer"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
