from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.conf import settings 
from django.conf.urls.static import static 
from .views import *

urlpatterns = [

    path('software-partner-info/', softwarePartnerList, name="software-partner-info"),
    path('software-info/', SoftwareList, name="software-info"),
    path('disable-partner-from-admin/', disablePartnerFromAdmin, name="disable-partner-from-admin"),
    path('enable-partner-from-admin/<int:id>', enablePartnerFromAdmin, name="enable-partner-from-admin"),
    path("add-partner-by-admin/", addPartnerByAdmin , name="add-partner-by-admin"),
    path("add-software-partner-by-admin/", addsoftwarePartnerByAdmin , name="add-software-partner-by-admin"),
    path("get-partner-business-details/", getPartnerBusinessDetails, name="get-partner-business-details"),
    path("edit-partner-by-admin/", editPartnerByAdmin, name="edit-partner-by-admin"),
    path("partner-by-sales/", partnerBySales, name="partner-by-sales/"),
    path('delete-partner/<int:id>',deletePartner, name="delete-partner"),
    path("partner-disabled/",disabledPartner, name="partner-disabled" ),
 	# path("partner-latest/", latestPartner, name="partner-latest"),
 	path('disapprove-partner/',disapprovePartner,name='disapprove-partner'),
  	path('send-partner-notice/',sendPartnerNotice,name="send-partner-notice"),
  	path('bulk-mail-partner/',BulkEmailPartner,name="bulk-mail-partner"),
    path('bulk-sms-partner/',BulkSmsPartner,name="bulk-sms-partner"),
    path('disable-partner-reason/', disablePartnerReason,name='disable-partner-reason'),
    path('delete-reasons/<int:id>', Delete_Reasons, name='delete-reasons'),
    path('delete-disabled-partner/<int:id>', Delete_disablePartner, name='delete-disabled-partner'),
    path('delete-partner-sms-email/<int:id>', deleteSmsEmail, name="delete-partner-sms-email"),

    path("partner-merchant-info/", Merchant_info_list, name="partner-merchant-info"),
    path("get-user-city-by-state/", GetCitiesByState, name="get-user-city-by-state"),
    path("delete-customer-record/<int:id>", Delete_customer_record, name="delete-customer-record"),
    path("partner-merchant-info/<str:mobile_no>", customer_info_by_mobile_no, name="customer-info-by-mobile-no"),
    
    path("send-partner-software-monthly-commission/", send_partner_software_monthly_commision, name="send-partner-software-monthly-commission"),

    path("check-contact-number/<int:id>", Check_Contact_number, name="check-contact-number"),
    path("edit-cust-info/", Edit_Cust_info, name="edit-cust-info"),
    path("add-merchant-by-partner/", addMerchantBypartner, name="add-merchant-by-partner"),
    path("merchant-info-view-partner/<int:id>/", viewMerchantInfo, name="merchant-info-view"),
    path("get-all-merchant-business-details/", getAllMerchantBusinessDetails , name="get-all-merchant-business-details"),
    path("edit-merchant-business-data/", editMerchantBusinessData, name="edit-merchant-business-data"),
    path('delete-merchant-business-data/<int:id>', deleteMerchantBusiness, name="delete-merchant-business-data"),
    path("merchant-info-view-record/<int:id>/", viewMerchantDetailsByPartner, name="merchant-info-view-record"),
    path("edit-merchant-of-software-partner/<int:id>/", viewMerchantDetailsOfsoftwarePartner, name="edit-merchant-of-software-partner"),
    path("view-merchant-info-all-records/<int:id>/", viewMerchantDetails_partner, name="view-merchant-info-all-records"),
    
    path("view-partner-info-record/<int:id>/", view_partner_record, name="view-partner-info-record"),
    path("delete-customer-by-owner/<int:id>", Delete_customer_by_owner, name="delete-customer-by-owner"),
    path('delete-merchant-by-owner/<int:id>', delete_merchant_by_owner, name="delete-merchant-by-owner"),
    # path("merchant-info-view-by-owner/<int:id>/", view_merchant_info_owner, name="merchant-info-view-by-owner"),
    path("get-all-merchant-business-details-by-owner/", getAllMerchantBusinessDetailsByOwner , name="get-all-merchant-business-details-by-owner"),
    path("edit-merchant-business-data-by-owner/", editMerchantBusinessData_byowner, name="edit-merchant-business-data-by-owner"),
    path("partner-info-edit-record/<int:id>/", edit_records_of_partner, name="partner-info-edit-record"),

    path("partner-info-edit-software-record/<int:id>/", edit_records_of_software_partner, name="partner-info-edit-software-record"),

    path('view-merchant-detail-by-partner/<int:id>/', viewMerchantsRecords, name="view-merchant-detail-by-partner"),
    path('view-merchant-analysis-by-partner/<int:id>/', viewMerchantsRecordsOfSoftwarePartner, name="view-merchant-analysis-by-partner"),

    path("disable-merchant-by-partner/", disableMerchantByPartner, name="disable-merchant-by-partner"),
    path('view-merchant-analysis/<int:id>/', viewMerchantsRecordsbypartner, name="view-merchant-analysis"),
    path("disable-merchant-in-partner/", disableMerchantByPartnerinpartner, name="disable-merchant-in-partner"),

    path('get-city-by-state-in-partner/', get_city_by_state_ids_in_partner_bulk_email, name="get-city-by-state-in-partner"),
    path("get-area-by-city-in-partner/", get_area_by_city_names_in_partner_bulk_email, name="get-area-by-city-in-partner"),
    path('get-template-by-header-in-partner/', get_template_by_header_in_partner, name="get-template-by-header-in-partner"),
    path('get-id-by-template-in-partner/', get_id_by_template_in_partner, name="get-id-by-template-in-partner"),

    path('get-merchant-city-by-state-in-partner/', get_merchant_city_by_state_names, name="get-merchant-city-by-state-in-partner"),

    path('get-merchant-area-by-city-in-partner/', get_merchant_area_by_city_names, name="get-merchant-area-by-city-in-partner"),

    path('partner-comision/', partner_comission, name="partner-comision"),

    path("view-partner-monthly-commision/<int:id>/", viewPartnerMonthlyCommision, name="view-partner-monthly-commision"),

    path("marketing-partner-monthly-commision/<int:id>/", viewMarketingPartnerMonthlyCommision, name="marketing-partner-monthly-commision"),

    path("view-software-partner-monthly-commision/<int:id>/", viewSoftwarePartnerMonthlyCommision, name="view-software-partner-monthly-commision"),

    path("add-commision-status/<int:id>/", AddPartnerCommionStatus, name="add-commision-status"),
    # Partner by type 

    path("get-partners-by-type/", GetpartnersbyType, name="get-partners-by-type"),

    # Subscription plans
    path("all-merchant-subscription-plans/", all_merchant_subscription_plans, name="all-merchant-subscription-plans"),

     # Promotional Plans
    path("all-merchant-promotional-subscription-plan/", all_merchant_promotions_subscription_plan,name="all-merchant-promotional-subscription-plan"),

    # Transactional Plans
    path("all-merchant-transactional-subscription-plan/", all_merchant_transactional_subscription_plan,name="all-merchant-transactional-subscription-plan"),

    # Add On's Plans
    path("all-merchant-add-on-plan/", all_merchant_add_on_plan, name="all-merchant-add-on-plan"),
    path("get-add-on-plan-details/<int:id>/", get_add_on_plan_details_by_id, name="get-add-on-plan-details"),

    path("get-excel-file-records/", StoreMerchantFromExcelFile, name="get-excel-file-records"),

    # partner-added-merchant
    path("merchant-field-by-partner-in-owner/",merchantChangeByOwner,name="merchant-field-by-partner-in-owner"),
    path("add-merchant-field-by-partner/",addmerchantfieldbypartner,name="add-merchant-field-by-partner")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

