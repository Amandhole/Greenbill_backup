from django.conf.urls import url
from django.urls import path, include  # add this
from rest_framework.routers import DefaultRouter
from .views import *


# router = DefaultRouter()
# router.register('customer-login', customerLogin, basename="customer-login")


urlpatterns = (
    path('parking-lot-merchant-login-api/', parkingLotMerchantLogin, name="parking-lot-merchant-login-api"),
    path('parking-lot-logout-api/', parkingLotLogout.as_view(), name="parking-lot-logout-api"),
    path('get-parking-lot-business-api/', getParkingLotBusinessList.as_view(), name="get-parking-lot-business-api"),
    path('get-parking-lot-vehicle-type-list-api/', getParkingLotVehicleTypeList.as_view(), name="get-parking-lot-vehicle-type-list-api"),
    path('get-parking-lot-space-api/', getParkingLotSpaceList.as_view(), name="get-parking-lot-space-api"),
    path('get-parking-lot-space-charges-api/', getParkingLotSpaceChargesList.as_view(), name="get-parking-lot-space-charges-api"),
    path('generate-parking-lot-invoice-number-api/', generateParkingLotInvoiceNumber.as_view(), name="generate-parking-lot-invoice-number-api"),
    path('save-parking-lot-bill-api/', saveParkingLotBill.as_view(), name="save-parking-lot-bill-api"),
    path('parking-lot-bill-list-api/', parkingLotbillList.as_view(), name="parking-lot-bill-list-api"),
    path('parking-lot-single-bill-details-api/', parkingLotSingleBillDetails.as_view(), name="parking-lot-single-bill-details-api"),
    path('parking-lot-dashboard-bill-calculation-api/', parkingLotDashboardBillCalculations.as_view(), name="parking-lot-dashboard-bill-calculation-api"),
    path('edit-parking-lot-bill-api/', editParkingLotBill.as_view(), name="edit-parking-lot-bill-api"),
    path('save-parking-lot-pass/', saveParkingLotPass.as_view(), name="save-parking-lot-pass"),
    path('save-parking-lot-bill-file/', saveParkingLotBillFile.as_view(), name="save-parking-lot-bill-file"),
    path('parking-lot-send-bill/', parkingLotSendBill, name="parking-lot-send-bill/"),
    path('parking-lot-bill/<str:id>/', parkingLotBill, name="parking-lot-bill/"),

    # path('parking-lot-bill1/<str:id>/', parkingLotBill1, name="parking-lot-bill1/"),

    path('parking-lot-business-details-api/', ParkingLotBusinessDetails.as_view(), name="parking-lot-business-details-api"),
    path('parking-lot-space-availability-details-api/', ParkingLotSpaceAvailabilityDetails.as_view(), name="parking-lot-space-availability-details-api"),
    path('get-all-parking-lot-pass-api/', GetAllPassesByUserId.as_view(), name="get-all-parking-lot-pass-api"),
    path('parking-add-bill-flag-api/', ParkingBillAddFlag.as_view(), name="parking-add-bill-flag-api"),

    path('parking-lot-exit-bill-list-api/', parkingLotExitbillList.as_view(), name="parking-lot-exit-bill-list-api"),
    path('set-parking-vehicle-as-exit-api/', SetParkingVehicleAsExit.as_view(), name="set-parking-vehicle-as-exit-api"),

    path('parking-lot-qr-check-api/', CheckParkingVehicleQRCode.as_view(), name="parking-lot-qr-check-api"),
    
    path('parking-pass-charges-api/', ParkingPassCharges.as_view(), name="parking-pass-charges-api"),

    path('parking-pass-companies-api/', ParkingPassCompanies.as_view(), name="parking-pass-companies-api"),

    path('save-parking-lot-pass-bill-api/', saveParkingLotPassBill.as_view(), name="save-parking-lot-pass-bill-api"),

    path('parking-pass-payment-list-api/', passPaymentList.as_view(), name="parking-pass-payment-list-api"),


    # Other Modules

    path('parking-delete-selected-flag-bill-api/', DeleteSelectedFlagBill.as_view(), name="parking-delete-selected-flag-bill-api"),
    path('parking-delete-flag-bill-api/', DeleteFlagBill.as_view(), name="parking-delete-flag-bill-api"),
    path('parking-flag-bill-list-api/', FlagBillList.as_view(), name="parking-flag-bill-list-api"),

    path('parking-manage-vehicle-type-api/', ManageVehicleType.as_view(), name="parking-manage-vehicle-type-api"),
    path('parking-manage-vehicle-type-list-api/', ManageVehicleTypeList.as_view(), name="parking-manage-vehicle-type-list-api"),
    path('parking-manage-vehicle-type-delete-api/', ManageVehicleTypeDelete.as_view(), name="parking-manage-vehicle-type-delete-api"),

    path('parking-manage-space-api/', ManageParkingSpace.as_view(), name="parking-manage-space-api"),
    path('parking-manage-space-list-api/', ManageParkingSpaceList.as_view(), name="parking-manage-space-list-api"),

    path('parking-manage-charges-api/', ManageCharges.as_view(), name="parking-manage-charges-api"),
    path('parking-manage-charges-list-api/', ManageChargesList.as_view(), name="parking-manage-charges-list-api"),  

    path('parking-bill-layout-settings-api/', ParkingBillLayoutSettings.as_view(), name="parking-bill-layout-settings-api"),

    path('parking-reject-bill/', reject_parking_bill, name="parking-reject-bill"),
    path('my-bill-parking-payment-link-success/', payment_link_success,name="my-bill-parking-payment-link-success"),
    path('my-bill-parking-payment-link-fail/', payment_link_fail,name="my-bill-parking-payment-link-fail"),
    # path('parking-lot-bill123/<str:id>/', parkingLotBill123, name="parking-lot-bill123/"),

    path("view-parking-ads-url/<str:id>/", view_parking_Lot_ads, name="view-parking-ads-url"),


    
)