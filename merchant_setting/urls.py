# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.urls import path, re_path, include
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [

    #Installtion steps
    path("merchant-software-installation-steps/", merchantSoftwareInstallationSteps, name="merchant-software-installation-steps"),

    # General Setting
    path("merchant-general-setting/", merchant_general_setting, name="merchant-general-setting"),
    path("merchant-general-setting-new/", merchant_general_setting_new, name="merchant-general-setting-new"),
    path("merchant-payment-settings/", merchant_payment_setting, name="merchant-payment-settings"),
    path("download-merchant-schedule-file/", download_merchant_schedule_file, name="download-merchant-schedule-file"),
    
    #Delete old bills setting
    path("delete-bills-setting/", delete_bills_by_days, name='delete-bills-setting'),
    path("select-payment-options/", select_payment_options, name='select-payment-options'),  

    # Users
    path('create-merchant-panel-user/', merchant_register_user_view, name="create-merchant-panel-user"),
    path('update-merchant-panel-user/', merchant_update_user_view, name="update-merchant-panel-user"),
    path('delete-merchant-panel-user/<int:id>', merchant_delete_user_view, name="delete-merchant-panel-user"),
    path('disable-merchant-panel-user/<int:id>', merchant_disable_user_view, name="disable-merchant-panel-user"),
    path('enable-merchant-panel-user/<int:id>', merchant_enable_user_view, name="enable-merchant-panel-user"),
    path("merchant-email-setting/", merchant_email_setting, name="merchant-email-setting"),
    path('merchant-sms-setting/', merchantSmsSetting, name="merchant-sms-setting"),
    path('merchant-sms-template-setting/', merchantSmstemplateSetting, name="merchant-sms-template-setting"),
    path('change-inactive-sms-header-status/<int:id>', changeSmsHeaderStatusDisable,name="change-active-sms-header-status"),
    path('change-active-sms-header-status/<int:id>', changeSmsHeaderStatusEnable,name="change-active-sms-header-status"),
    path('delete-sms-header/<int:id>', deleteSmsHeader, name="delete-sms-header"),
    path('change-user-password/', merchantchangeuserpassword,name="change-user-password"),
    # path('active-sms-template-status/<int:id>', activesmstemplate,name="active-sms-header-status"),
    
    path('delete-sms-template-by-merchant/<int:id>', deleteSmstemplatebymerchant,name="delete-sms-template-by-merchant"),

    #Petrol Pump
    path('merchant-petrol-pump-details/', petrolPumpDetails, name="merchant-petrol-pump-details"),
    path('get-petrol-pump-product-details/', getPetrolPumpProductDetail, name="get-petrol-pump-product-details"),
    path('edit-petrol-pump-product-details/', editPetrolPumpProductDetail, name="edit-petrol-pump-product-details"),
    path('delete-petrol-pump-product/<int:id>', deletePetrolPumpProduct, name="delete-petrol-pump-product"),
    path("petrol-pump-app-setting/", petrol_pump_app_setting, name="petrol-pump-app-setting"),

    path('add-petrol-nozzle/', addPetrolNozzle, name="add-petrol-nozzle"),
    path('get-petrol-nozzle-details/', getPetrolNozzleDetail, name="get-petrol-nozzle-details"),
    path('edit-petrol-nozzle/', editPetrolNozzle, name="edit-petrol-nozzle"),
    path('delete-petrol-nozzle/<int:id>', deletePetrolNozzle, name="delete-petrol-nozzle"),

    path('petrol-pump-flag-bills/', petrol_pump_flag_bills, name="petrol-pump-flag-bills"),
    path('delete-petrol-pump-flag-bill/<int:id>', deletePetrolPumpFlagBill, name="delete-petrol-pump-flag-bill"),
    path('delete-selected-petrol-pump-flag-bills/', deleteSelectedPetrolPumpFlagBills, name="delete-selected-petrol-pump-flag-bills"),

    path('update-petrol-rating/<str:id>/', update_petrol_rating_view, name="update-petrol-rating"),
    path('get-header-footer-detals/',getHeaderFooterDetail,name="get-header-footer-detals"),



    #Parking Lot
    path("add-vehicle-type/", addVehicleType, name="add-vehicle-type"),
    path("delete-vehicle-type/<int:id>", deleteVehicleType, name="delete-vehicle-type"),
    path('add-parking-space/', addParkingSpace, name="add-parking-space"),
    path('get-parking-lot-space-details/', getParkingLotSpaceDetails, name="get-parking-lot-space-details"),
    path('edit-parking-lot-space-details/', editParkingLotSpaceDetails, name="edit-parking-lot-space-details"),
    path('delete-parking-lot-space/<int:id>', deleteParkingLotSpace, name="delete-parking-lot-space"),
    path('add-parking-space-charges/', addParkingSpaceCharges, name="add-parking-space-charges"),
    path('get-parking-space-charges/', getParkingSpaceCharges, name="get-parking-space-charges"),
    path('edit-parking-space-charges/', editParkingSpaceCharges, name="edit-parking-space-charges"),
    path('delete-parking-space-charges/<int:id>', deleteParkingSpaceCharges, name="delete-parking-space-charges"),
    path("parking-app-setting/", parking_app_setting, name="parking-app-setting"),

    path('parking-flag-bills/', parking_flag_bills, name="parking-flag-bills"),
    path('delete-parking-flag-bill/<int:id>', deletePArkingFlagBill, name="delete-parking-flag-bill"),

    path('delete-selected-parking-flag-bills/', deleteSelectedParkingFlagBills, name="delete-selected-parking-flag-bills"),


    path('update-parking-rating/<str:id>/', update_parking_rating_view, name="update-parking-rating"),
    path("exit-parked-vehicles/", exitParkedVehicles, name="exit-parked-vehicles"),


    path("merchant-business-logo-remove/", merchant_business_logo_remove, name="merchant-business-logo-remove"),
    path("merchant-business-stamp-remove/", merchant_business_stamp_remove, name="merchant-business-stamp-remove"),
    path("merchant-digital-signature-remove/", merchant_digital_signature_remove, name="merchant-digital-signature-remove"),
    

    path('addon-petrol-pump-details/', addonPetrolPumpDetails, name="addon-petrol-pump-details"),
    path('get-addon-petrol-pump-product-details/', getAddonPetrolPumpProductDetail, name="get-addon-petrol-pump-product-details"),
    path('edit-addon-petrol-pump-product-details/', editAddonPetrolPumpProductDetail, name="edit-addon-petrol-pump-product-details"),
    path('delete-addon-petrol-pump-product/<int:id>', deleteAddonPetrolPumpProduct, name="delete-addon-petrol-pump-product"),
    path("merchant-passes/",addParkingPassCharges,name="merchant-passes"),
    path("delete-parking-pass/<int:id>",DeletePass,name="delete-parking-pass"),

    path("delete-parking-pass-charges/<int:id>",DeleteParkingPassCharges,name="delete-parking-pass-charges"),
    path("get-all-parking-pass-charges/",GetAllParkingPassCharges,name="get-all-parking-pass-charges"),
    
    path("delete-parking-pass-charges/<int:id>", deleteParkingPassCharges, name="delete-parking-pass-charges"),

    path("manage-companies/",addPassCompaniesName,name="manage-companies"),
    path("delete-pass-company/<int:id>", deletePassCompany, name="delete-pass-company"),


    # upload cropped logo/signature/stamp
    path("merchant-cropped-logo-upload/", merchant_cropped_logo_upload,name="merchant-cropped-logo-upload"),
    path("merchant-cropped-stamp-upload/", merchant_cropped_stamp_upload,name="merchant-cropped-stamp-upload"),
    path("merchant-cropped-signature-upload/", merchant_cropped_signature_upload,name="merchant-cropped-signature-upload"),
    


    path("flag-reason/", addFlagReason,name="flag-reason"),
    path("delete-flag-reason/<int:id>", deleteFlagReason, name="delete-flag-reason"),
    path("add-petrol-nozzle-count/", addPetrolNozzleCount, name="add-petrol-nozzle-count"),

    
   
]
