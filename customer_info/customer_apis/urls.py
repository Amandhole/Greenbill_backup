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

    #Green Point
    path('get-customer-green-points-api/', getCustomerGreenPoints.as_view(), name="get-customer-green-points-api"),

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
    path('get-bill-by-bill-id-api/', getBillByBillId.as_view(), name="get-bill-by-bill-id-api"),
    path('get-bill-categories-list-by-customer-id-api/', getBillCategoriesListByCustomerId.as_view(), name="get-bill-categories-list-by-customer-id-api"),
    path('get-merchant-business-list-by-customer-id-api/', getMerchantBusinessListByCustomerId.as_view(), name="get-merchant-business-list-by-customer-id-api"),

    #Parking Pass
    path('parking-lot-pass-list-api/', parkingPassList.as_view(), name="parking-lot-pass-list-api"),

    
    
)