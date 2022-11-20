from django.conf.urls import url
from django.urls import path, include  # add this
from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()
# router.register('customer-login', customerLogin, basename="customer-login")


urlpatterns = (
    path('merchant-login-api/', merchantLogin, name="merchant-login-api"),
    path('merchant-change-password-api/', merchantChangePassword.as_view(), name="merchant-change-password-api"),
    path('get-merchant-business-category-api/', getMerchantBusinessCategory, name="get-merchant-business-category-api"),
    path('validate-merchant-mobile-number-api/', validateMerchantMobileNumber, name="validate-merchant-mobile-number-api"),
    path('generate-otp-merchant-api/', generateOtpMerchnat, name="generate-otp-merchant-api"),
    path('otp-validate-merchant-api/', otpValidateMerchant, name="otp-validate-merchant-api"),
    path('merchant-register-api/', merchantRegister, name="merchant-register-api"),
    path('generate-otp-forgot-password-merchant-api/', generateOtpMerchantForgotPassword, name="generate-otp-forgot-password-merchant-api"),
    path('forgot-password-merchant-api/', forgotPasswordMerchant, name="forgot-password-merchant-api"),
    path('set-merchant-profile-api/', setMerchantProfileData.as_view(), name="set-merchant-profile-api"),
    path('get-merchant-details-api/', getMerchantDetails.as_view(), name="get-merchant-details-api"),
    path('remove-merchant-profile-image-api/', removeMerchantProfileImage, name="remove-merchant-profile-image-api"),
    path('get-merchant-profile-image-api/', getMerchantProfileImage.as_view(), name="get-merchant-profile-image-api"),
    path('set-merchant-profile-image-api/', setMerchantProfileImage.as_view(), name="set-merchant-profile-image-api"),
    path('get-merchant-general-setting-api/', getMerchantGeneralSetting.as_view(), name="get-merchant-general-setting-api"),
    path('set-merchant-general-setting-api/', setMerchantGeneralSetting.as_view(), name="set-merchant-general-setting-api"),
    path('merchant-upload-cancel-check-api/',MerchantUploadCancelCheck.as_view(), name='merchant-upload-cancel-check-api'),
    path('remove-digital-signature-api/',RemoveDigitalSignature.as_view(), name='remove-digital-signature-api'),
    path('remove-business-logo-api/',RemoveBusinessLogo.as_view(), name='remove-business-logo-api'),
    path('get-merchant-businesses-api/', getMerchantBusinesses.as_view(), name="get-merchant-businesses-api"),
    path('add-dm-enquiry-api/', addDMenquiry.as_view(), name="add-dm-enquiry-api"),
    path('get-customer-info-api/', getCustomerInfo.as_view(), name="get-customer-info-api"),
    path('get-bills-by-mobile-no-api/', getBillsByMobileNo.as_view(), name="get-bills-by-mobile-no-api"),
    path('get-cash-memo-by-mobile-no-api/', getCashMemoByMobileNo.as_view(), name="get-cash-memo-by-mobile-no-api"),
    path('get-receipt-by-mobile-no-api/', getReceiptByMobileNo.as_view(), name="get-receipt-by-mobile-no-api"),

    path('customer-info-send-sms-api/', customerInfoSendSms.as_view(), name="customer-info-send-sms-api"),
    path('get-bill-info-list-api/', getBillInfoList.as_view(), name="get-bill-info-list-api"),
    path('bill-info-send-sms-api/', BillInfoSendSms.as_view(), name="bill-info-send-sms-api"),
    path('get-merchant-referral-code-api/', getMerchantReferralCode.as_view(), name="get-merchant-referral-code-api"),

    path('create-merchant-user-api/', createMerchantUser.as_view(), name="create-merchant-user-api"),
    path('merchant-user-role-api/', MerchantUserRole.as_view(), name="merchant-user-role-api"),
    path('merchant-users-api/', MerchantUsers.as_view(), name="merchant-users-api"),

    # path('get-token-authentication-api/', get_token_key, name="get-token-authentication-api")

    # Dashboard Merchant Parking Business
    path('parking-merchant-dashboard-header-calulations-api/', ParkingMerchantDashboardHeaderCalulations.as_view(), name="parking-merchant-dashboard-header-calulations-api"),
    path('parking-merchant-vehicle-type-wise-calulations-graph-api/', ParkingMerchantVehicleTypeWiseCalulationsGraph.as_view(), name="parking-merchant-vehicle-type-wise-calulations-graph-api"),
    path('parking-merchant-vehicle-type-wise-bills-graph-api/', ParkingMerchantVehicleTypeWiseBillsGraph.as_view(), name="parking-merchant-vehicle-type-wise-bills-graph-api"),
    path('parking-merchant-user-analysis-api/', ParkingMerchantUserAnalysis.as_view(), name="parking-merchant-user-analysis-api"),
    path('parking-merchant-session-graph-api/', ParkingMerchantSessionGraph.as_view(), name="parking-merchant-session-graph-api"),
    

    # dashboard Merchant Petrol Business
    path('petrol-merchant-dashboard-header-calulations-api/', PetrolMerchantDashboardHeaderCalulations.as_view(), name="petrol-merchant-dashboard-header-calulations-api"),
    path('petrol-merchant-product-sales-graph-api/', PetrolMerchantProductSalesGraph.as_view(), name="petrol-merchant-product-sales-graph-api"),
    path('petrol-merchant-add-on-sales-graph-api/', PetrolMerchantAddOnSalesGraph.as_view(), name="petrol-merchant-add-on-sales-graph-api"),
    path('petrol-merchant-user-analysis-api/', PetrolMerchantUserAnalysis.as_view(), name="petrol-merchant-user-analysis-api"),
    path('petrol-merchant-session-graph-api/', PetrolMerchantSessionGraph.as_view(), name="petrol-merchant-session-graph-api"),

    #card-details 
    path('merchant-card-design-api/', merchantcard, name="merchant-card-design-api"),
    path('merchant-card-details-api/', merchantcarddetails, name="merchant-card-details-api"),


    path('suggest-business-api/', SuggestBusiness_API.as_view(), name = "suggest-business-api"),
    path('suggest-business-list-api/', SuggestBusinessList_API.as_view(), name = "suggest-business-list-api"),

    # Suggest a Brand
    path('merchant-suggest-brand-api/', SuggestBrandAPI.as_view(), name="merchant-suggest-brand-api"),

    # Feedback
    path('merchant-feedback-api/', FeedbackAPI.as_view(), name="merchant-feedback-api"),

    # Cash Memo
    path('merchant-create-cash-memo-api/', CreateCashMemoAPI.as_view(), name="merchant-create-cash-memo-api"), # Create Cash Memo
    path('get-stamp-data-api/', get_stamp_data.as_view(), name="get-stamp-data-api"), # return stamp id and name
    path('merchant-cash-memo-list-api/', CashMemoListAPI.as_view(), name="merchant-cash-memo-list-api"), # Cash Memo List
    path('merchant-cash-memo-delete-api/', CashMemoDeleteAPI.as_view(), name="merchant-cash-memo-delete-api"), # Cash Memo Delete
    path('merchant-cash-memo-send-api/', CashMemoSendAPI.as_view(), name="merchant-cash-memo-send-api"), # Cash Meno SMS Send
    path('merchant-cash-memo-save-template/', CashMemoSaveTemplate.as_view(), name="merchant-cash-memo-save-template"), # Cash Meno save template
    path('cash-memo-template-existornot/', CashMemoTemplateExist.as_view(), name="cash-memo-template-existornot"), # Cash Meno Template exist or not


    # Receipt
    path('merchant-create-receipt-api/', CreateReceiptAPI.as_view(), name="merchant-create-receipt-api"), # Create Receipt
    path('merchant-receipt-list-api/', ReceiptListAPI.as_view(), name="merchant-receipt-list-api"), # Receipt List
    path('merchant-receipt-delete-api/', ReceiptDeleteAPI.as_view(), name="merchant-receipt-delete-api"), # Receipt Delete
    path('merchant-receipt-send-api/', ReceiptSendAPI.as_view(), name="merchant-receipt-send-api"), # Cash Meno SMS Send
    path('merchant-receipt-save-template/', ReceiptSaveTemplate.as_view(), name="merchant-receipt-save-template"), # Receipt save template
    path('receipt-template-existornot/', ReceiptTemplateExist.as_view(), name="receipt-template-existornot"), # Receipt Template Exist or not


    # Supports & Faqs
    path('merchant-get-support-and-faqs-modules-api/', GetSupportAndFaqsModulesAPI.as_view(), name="merchant-get-support-and-faqs-modules-api"), # Get Modules
    path('merchant-get-support-and-faqs-data-api/', GetSupportAndFaqsDataAPI.as_view(), name="merchant-get-support-and-faqs-data-api"), # Get Modules

    # Coupons
    path('merchant-create-and-update-coupon-api/', CreateandUpdateCouponAPI.as_view(), name="merchant-create-and-update-coupon-api"), # Create & update Coupons
    path('merchant-coupon-list-api/', MerchantCouponListAPI.as_view(), name="merchant-coupon-list-api"), # Coupons List
    path('merchant-delete-coupon-api/', MerchantDeleteCouponAPI.as_view(), name="merchant-delete-coupon-api"), # Coupon Delete
    path('get-merchant-clicks-of-coupon-api/', GetMerchantClicksOfCouponsAPI.as_view(), name="get-merchant-clicks-of-coupon-api"), #Coupons CLicks

    # Offers
    path('merchant-get-offers-api/', MerchantGetOffersAPI.as_view(), name="merchant-get-offers-api"), # Get Offers
    path('get-merchant-clicks-of-offers-api/', GetMerchantClicksOfOffersAPI.as_view(), name="get-merchant-clicks-of-offers-api"), #Offers CLicks
    path('merchant-create-and-update-offers-api/', MerchantCreateandUpdateOffersAPI.as_view(), name="merchant-create-and-update-offers-api"), # Get Offers
    path('merchant-offers-list-api/', MerchantOffersListAPI.as_view(), name="merchant-offers-list-api"), # Coupons List
    path('merchant-delete-offers-api/', MerchantDeleteOffersAPI.as_view(), name="merchant-delete-offers-api"), # Coupon Delete


    # Payments
    path("merchant-create-payment-link-api/", CreatePaymentLink.as_view(), name="merchant-create-payment-link-api"), # Payment Link Create
    path("merchant-payment-link-list-api/", PaymentLinkList.as_view(), name="merchant-payment-link-list-api"), # Payment Link List
    path("merchant-payment-link-send-api/", PaymentLinkSend.as_view(), name="merchant-payment-link-send-api"), # Payment Link Send
    path("merchant-payment-link-delete-api/", PaymentLinkDelete.as_view(), name="merchant-payment-link-delete-api"), # Payment Link Delete

    path("merchant-get-payment-history-api/", GetPaymentHistory.as_view(), name="merchant-get-payment-history-api"),
    path("merchant-get-payment-received-api/", GetPaymentReceived.as_view(), name="merchant-get-payment-received-api"),

    path('merchant-create-and-update-payment-setting-api/', CreateMerchantPaymentSetting.as_view(), name="merchant-create-and-update-payment-setting-api"),

    path('show-merchant-payment-setting-api/', ShowMerchantPaymentSetting.as_view(), name="show-merchant-payment-setting-api"),


    # Subscription
    path("merchant-get-subscription-details-api/", GetSubscriptionDetails.as_view(), name="merchant-get-subscription-details-api"), # Get Details
    path("merchant-get-subscription-history-api/", GetSubscriptionHistory.as_view(), name="merchant-get-subscription-history-api"), # Get history
    path("merchant-get-subscription-plans-api/", GetSubscriptionPlans.as_view(), name="merchant-get-subscription-plans-api"), # Get Subscription Plans
    path("merchant-get-promotional-sms-subscription-api/", GetPromotionalSMSSubscription.as_view(), name="merchant-get-promotional-sms-subscription-api"), # Get Subscription Plans
    path("merchant-get-transactional-sms-subscription-api/", GetTransactionalSMSSubscription.as_view(), name="merchant-get-transactional-sms-subscription-api"), # Get transactional sms Subscription Plans
    path("merchant-get-addon-recharge-api/", GetAddOnRecharge.as_view(), name="merchant-get-addon-recharge-api"), # Get AddOn Recharge Plans

    path("merchant-get-all-addon-amounts-api/", GetAddOnAmounts.as_view(), name="merchant-get-all-addon-amounts-api"), # Get All AddOn Amounts

    path("get-subscription-recharge-history-details-api/", GetRechargeHistoryDetails.as_view(), name="get-subscription-recharge-history-details-api"), # Recharge History Details

    path("merchant-referral-code-validate-api/", ReferralCodeValidateMerchant, name="merchant-referral-code-validate-api"), # Referral Code Validate

    path("merchant-get-businessname-by-category-api/", GetBusinessNameByCategory.as_view(), name="merchant-get-businessname-by-category-api"), # Get Business name by category

    path("merchant-get-received-bill-api/", GetReceivedBill.as_view(), name="merchant-get-received-bill-api"),
    path("merchant-send-received-bill-api/", SendReceivedBill.as_view(), name="merchant-get-received-bill-api"),


    path("merchant-get-rejected-bill-api/", GetRejectedBill.as_view(), name="merchant-get-rejected-bill-api"),

    path("merchant-delete-bill-api/", DeleteRejectedBill.as_view(), name="merchant-delete-bill-api"),

    path("merchant-get-bill-rating-api/", GetBillRating.as_view(), name="merchant-get-bill-rating-api"),

    path("view-merchant-analysis-rating-graph-api/", ViewRatingAnalysisGraph.as_view(), name="view-merchant-analysis-rating-graph-api"),

    # Dashboard for Other Business
    path("merchant-get-dashboard-details-api/", GetDashboardDetails.as_view(), name="merchant-get-dashboard-details-api"),
    path("merchant-billing-analysis-graph-api/", MerchantBillingAnalysisGraphAPI.as_view(), name="merchant-billing-analysis-graph-api"),
    path("merchant-digital-billing-graph-api/", MerchantDigitalBillingGraphAPI.as_view(), name="merchant-digital-billing-graph-api"),
    path("merchant-coupons-details-graph-api/", MerchantCouponsDetailsGraphAPI.as_view(), name="merchant-coupons-details-graph-api"),
    path("merchant-offers-details-graph-api/", MerchantOffersDetailsGraphAPI.as_view(), name="merchant-offers-details-graph-api"),
    path("merchant-overall-customer-analysis-graph-api/", MerchantOverallCustomerAnalysisGraphAPI.as_view(), name="merchant-overall-customer-analysis-graph-api"),

    path('other-business-merchant-session-graph-api/', OtherBusinessMerchantSessionGraph.as_view(), name="other-business-merchant-session-graph-api"),

    path("other-business-session-datewise-graph-api/", OtherBusinessBillSessionDatewiseGraph.as_view(), name="other-business-session-datewise-graph-api"),

    # Dashboard for Other Business EXE details
    path("merchant-exe-details-api/", GetMerchantExeDetails.as_view(), name="merchant-exe-details-api"),


    #Bulk SMS
    path("merchant-send-bulksms-api/", SendBulkSMS.as_view(), name="merchant-send-bulksms-api"),
    path("merchant-get-SMSHeaderList-api/",GetSMSHeaderList.as_view(), name="merchant-get-SMSHeaderList-api"),
    path("merchant-get-SMSTemplateList-api/",GetSMSTemplateList.as_view(), name="merchant-get-SMSTemplateList-api"),

    path("get-customer-state/",GetCustomerState.as_view(), name="get-customer-state"),

    path("get-customer-count-by-state-city-area-api/",GetCustomerCountByStateCityArea.as_view(), name="get-customer-count-by-state-city-area-api"),
    
    path("get-customer-city-by-state/",GetCustomerCityByState.as_view(), name="get-customer-city-by-state"),
    path("get-customer-area-by-city/",GetCustomerAreaByCity.as_view(), name="get-customer-area-by-city"),

    #payment Success
    path("merchant-subscription-purchased-success/", SubscriptionPurchasedSuccess.as_view(), name="merchant-subscription-purchased-success"),
    path("merchant-subscription-purchased-failed/", SubscriptionPurchasedFailed.as_view(), name="merchant-subscription-purchased-failed"),

    path("merchant-subscription-buy-btn-info/", SubscriptionBuyButtonInfo.as_view(), name="merchant-subscription-buy-btn-info"),

    path("merchant-parking-lot-pass-list-api/", MerchantParkingPassList.as_view(), name="merchant-parking-lot-pass-list-api"),

    #notice board
    path("get-merchant-notice-board-list-api/", MerchantNoticeBoardList.as_view(), name="get-merchant-notice-board-list-api"),

    path("get-user-cities-by-states-api/", GetUserCitiesByStates, name="get-user-cities-by-states-api"),

    path('hit-number-of-views/',HitNumberOfViewsAPI, name="hit-number-of-views"),
    path('merchant-analysis-api/' ,MerchantAnalysisApi , name='merchant-analysis-api')

)
