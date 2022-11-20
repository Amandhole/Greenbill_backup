from django.conf.urls import url
from django.urls import path, include  # add this
from rest_framework.routers import DefaultRouter
from .views import *



# router = DefaultRouter()
# router.register('customer-login', customerLogin, basename="customer-login")


urlpatterns = (
    path('customer-login-api/', customerLogin, name="customer-login-api"),
    path('customer-change-password-api/', customerChangePassword.as_view(), name="customer-change-password-api"),
    path('set-customer-profile-api/', setCustomerProfileData.as_view(), name="set-customer-profile-api"),
    path('validate-customer-mobile-number-api/', validateCustomerMobileNumber, name="validate-customer-mobile-number-api"),
    path('generate-otp-customer-api/', generateOtpCustomer, name="generate-otp-customer-api"),
    path('otp-validate-customer-api/', otpValidateCustomer, name="otp-validate-customer-api"),
    path('customer-register-api/', customerRegister, name="customer-register-api"),
    path('generate-otp-forgot-password-customer-api/', generateOtpCustomerForgotPassword, name="generate-otp-forgot-password-customer-api"),
    path('forgot-password-customer-api/', forgotPasswordCustomer, name="forgot-password-customer-api"),
    path('get-customer-details-api/', getCustomerDetails.as_view(), name="get-customer-details-api"),
    path('remove-customer-profile-image-api/', removeCustomerProfileImage, name="remove-customer-profile-image-api"),
    path('get-customer-profile-image-api/', getCustomerProfileImage.as_view(), name="get-customer-profile-image-api"),
    path('set-customer-profile-image-api/', setCustomerProfileImage.as_view(), name="set-customer-profile-image-api"),
    
    #loyeltypoint 
    path('get-loyelty-point-api', GetCustomerLoyeltyPoints, name="get-loyelty-point-api"),
    #Green Point
    path('get-customer-green-points-api/', getCustomerGreenPoints.as_view(), name="get-customer-green-points-api"),
    path('green-points-earned-history-api/', GreenPointsEarnedHistoryAPI.as_view(), name="green-points-earned-history-api"),

    #Shopping Analysis
    path('get-shopping-analysis-by-category-api/', getShoppingAnalysisByCategory.as_view(), name="get-shopping-analysis-by-category-api"),
    path('get-shopping-analysis-by-merchant-api/', getShoppingAnalysisByMerchant.as_view(), name="get-shopping-analysis-by-merchant-api"),

    #Customer QR
    path('generate-customer-qr-api/', generateQRCustomer.as_view(), name="generate-customer-qr-api"),
    path('list-customer-qr-api/', listQRCustomer.as_view(), name="list-customer-qr-api"),
    path('edit-customer-qr-api/', editQRCustomer.as_view(), name="edit-customer-qr-api"),

    #Customer Bills
    path('get-bill-categories-api/', getBillCategoriesList.as_view(), name="get-bill-categories-api"),
    path('get-bill-tags-api/', getBillTagsList.as_view(), name="get-bill-tags-api"),
    path('get-bill-business-list-api/', getMerchantBusinessList.as_view(), name="get-bill-business-list-api"),
    path('get-customer-bill-list-api/', getCustomerBillList.as_view(), name="get-customer-bill-list-api"),
    path('add-customer-bill-api/', addCustomerBill.as_view(), name="add-customer-bill-api"),
    path('edit-customer-bill-api/', editCustomerBill.as_view(), name="edit-customer-bill-api"),
    path('delete-customer-bill-api/', deleteCustomerBill.as_view(), name="delete-customer-bill-api"),
    path('download-customer-bill-api/', downloadCustomerBill.as_view(), name="download-customer-bill-api"),
    path('get-bill-by-merchant-store-api/', getBillByMerchantStore.as_view(), name="get-bill-by-merchant-store-api"),
    path('get-bill-by-bill-category-api/', getBillByBillCategory.as_view(), name="get-bill-by-bill-category-api"),

    path('share-customer-bill-api/', ShareBillTOCustomer.as_view(), name="share-customer-bill-api"),
    path('get-shared-customer-bill-api/', GetSharedCustomersBill.as_view(), name="get-shared-customer-bill-api"),

    path('get-bill-by-bill-id-api/', getBillByBillId.as_view(), name="get-bill-by-bill-id-api"),
    path('get-bill-categories-list-by-customer-id-api/', getBillCategoriesListByCustomerId.as_view(), name="get-bill-categories-list-by-customer-id-api"),
    path('get-merchant-business-list-by-customer-id-api/', getMerchantBusinessListByCustomerId.as_view(), name="get-merchant-business-list-by-customer-id-api"),
    
    path('get-merchant-business-by-customer-id-api/', getMerchantBusinessByCustomerID.as_view(), name="get-merchant-business-by-customer-id-api"),

    path('get-bill-by-bill-tags-api/', getBillByBillTags.as_view(), name="get-bill-by-bill-tags-api"),
    path('get-tags-list-by-customer-id-api/', getTagsListByCustomerId.as_view(), name="get-tags-list-by-customer-id-api"),

    path('send-bill-by-merchant-store-api/', SendBillByMerchantStore.as_view(), name="send-bill-by-merchant-store-api"),

    path('store-favourite-bill-api/', SaveFavouriteBill.as_view(), name="store-favourite-bill-api"),

    #Parking Pass
    path('parking-lot-pass-list-api/', parkingPassList.as_view(), name="parking-lot-pass-list-api"),

    
    path('customer-bill-view-api/', BillViewAPI.as_view(), name="customer-bill-view-api"),

    # Coupons
    path('get-coupons-api/', GetCouponsAPI.as_view(), name="get-coupons-api"),
    path('get-coupons-redeem-history-api/', GetCouponsRedeemHistoryAPI.as_view(), name="get-coupons-redeem-history-api"),
    path('redeem-coupon-api/', RedeemCouponAPI.as_view(), name="redeem-coupon-api"),
    path('coupon-number-of-views/',CouponNumberOfViewsAPI.as_view(), name="coupon-number-of-views"),

    # Share a Word
    path('customer-share-a-word-api/', ShareWordAPI.as_view(), name="customer-share-a-word-api"),

    # Suggest a Brand
    path('customer-suggest-brand-api/', SuggestBrandAPI.as_view(), name="customer-suggest-brand-api"),

    # Feedback
    path('customer-feedback-api/', FeedbackAPI.as_view(), name="customer-feedback-api"),
    path('customer-rating-api/', RatingAPI.as_view(), name="customer-rating-api"),
    path('view-customer-rating-analysis-graph-api/', ViewCustomerRatingAnalysisGraph.as_view(), name="view-customer-rating-analysis-graph-api"),


    # Supports & Faq's
    path('get-support-and-faqs-modules-api/', GetSupportAndFaqsModulesAPI.as_view(), name="get-support-and-faqs-modules-api"),
    path('get-support-and-faqs-data-api/', GetSupportAndFaqsDataAPI.as_view(), name="get-support-and-faqs-data-api"),

    # Referral Code
    path('get-customer-referral-code-api/', getCustomerReferralCode.as_view(), name="get-customer-referral-code-api"),

    # Seen status update
    path('customer-bill-seen-status-update-api/', UpdateSeenStatusAPI.as_view(), name="customer-bill-seen-status-update-api"),

    # Offers
    path('customer-get-offers-api/', CustomerGetOffersAPI.as_view(), name="customer-get-offers-api"),

    path("customer-referral-code-validate-api/", ReferralCodeValidateCustomer, name="customer-referral-code-validate-api"), # Referral Code Validate
        
    path("customer-get-offers-api_test/", CustomerGetOffersAPI_test.as_view(), name="customer-get-offers-api_test"), # Referral Code Validate

    path('customer-payment-history-api/',CustomerPaymentHistoryAPI.as_view(),name="customer-payment-history-api"), # Payment History

    path('get-merchant-business-by-category-id-api/', GetMerchantBusinessByCategoryIdAPI.as_view(),name="get-merchant-business-by-category-id-api"), # Get merchant by category

    #cash memo
    path('customer-cash-memo-list-api/', CustomerCashMemoListAPI.as_view(), name="customer-cash-memo-list-api"), # Cash Memo List

    # Receipt
    path('customer-receipt-list-api/', CustomerReceiptListAPI.as_view(), name="customer-receipt-list-api"), # Receipt List

    # Customer-info-api
    # path('customer_info_api/',cust_info_api,name = "cust_info_api")
    path('cust_info_api/',cust_info_api, name = "cust_info_api")

)