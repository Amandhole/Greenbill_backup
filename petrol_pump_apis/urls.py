from django.conf.urls import url
from django.urls import path, include  # add this
from rest_framework.routers import DefaultRouter
from .views import *


# router = DefaultRouter()
# router.register('customer-login', customerLogin, basename="customer-login")


urlpatterns = (
    path('petrol-pump-merchant-login-api/', petrolPumpMerchantLogin, name="petrol-pump-merchant-login-api"),
    path('petrol-logout-api/', petrolLogout.as_view(), name="petrol-logout-api"),
    path('get-petrol-pump-business-api/', getPetrolPumpBusinessList.as_view(), name="get-petrol-pump-business-api"),
    path('get-petrol-pump-product-list-api/', getPetrolPumpProductList.as_view(), name="get-petrol-pump-product-list-api"),
    path('save-petrol-pump-bill-api/', savePetrolPumpBill.as_view(), name="save-petrol-pump-bill-api"),
    path('generate-invoice-number-api/', generatePetrolPumpInvoiceNumber.as_view(), name="generate-invoice-number-api"),
    path('bill-list-api/', billList.as_view(), name="bill-list-api"),
    path('single-bill-details-api/', singleBillDetails.as_view(), name="single-bill-details-api"),
    path('dashboard-bill-calculation-api/', dashboardBillCalculations.as_view(), name="dashboard-bill-calculation-api/"),
    path('save-petrol-pump-bill-file/', savePetrolPumpBillFile.as_view(), name="save-petrol-pump-bill-file"),
    path('petrol-pump-send-bill/', petrolPumpSendBill, name="petrol-pump-send-bill"),
    path('petrol-pump-bill/<str:id>/', petrolPumpBill, name="petrol-pump-bill/"),
    path('petrol-pump-business-details-api/', PetrolPumpBusinessDetails.as_view(), name="petrol-pump-business-details-api"),
    path('addons-product-list-api/', AddonsProductList.as_view(), name="addons-product-list-api"),
    path('get-petrol-nozzle-list-api/', PetrolNozzleList.as_view(), name="get-petrol-nozzle-list-api"),
    path('petrol-pump-add-bill-flag-api/', PetrolBillAddFlag.as_view(), name="petrol-pump-add-bill-flag-api"),
    path('flag-bill-reason-api/', getflagReason.as_view(), name="flag-bill-reason-api"),

    # Other Modules
    path('petrol-manage-product-api/', ManageProduct.as_view(), name="petrol-manage-product-api"),
    path('petrol-manage-product-list-api/', ManageProductList.as_view(), name="petrol-manage-product-list-api"),

    path('petrol-manage-nozzle-api/', ManageNozzle.as_view(), name="petrol-manage-nozzle-api"),
    path('petrol-nozzle-count-api/', ManageNozzleCount.as_view(), name="petrol-nozzle-count-api"),

    path('petrol-ad-on-products-api/', AdOnProducts.as_view(), name="petrol-ad-on-products-api"),
    path('petrol-ad-on-product-list-api/', AdOnProductList.as_view(), name="petrol-ad-on-product-list-api"),

    path('petrol-delete-selected-flag-bill-api/', DeleteSelectedFlagBill.as_view(), name="petrol-delete-selected-flag-bill-api"),
    path('petrol-delete-flag-bill-api/', DeleteFlagBill.as_view(), name="petrol-delete-flag-bill-api"),
    path('petrol-flag-bill-list-api/', FlagBillList.as_view(), name="petrol-flag-bill-list-api"),

    path('petrol-reject-bill/', reject_petrol_bill, name="petrol-reject-bill"),
    path('my-bill-petrol-payment-link-success/', payment_link_success,name="my-bill-petrol-payment-link-success"),
    path('my-bill-petrol-payment-link-fail/', payment_link_fail,name="my-bill-petrol-payment-link-fail"),
    path("view-petrol-pump-ads-url/<str:id>/", view_petrol_pump_ads, name="view-petrol-pump-ads-url"),
    

)