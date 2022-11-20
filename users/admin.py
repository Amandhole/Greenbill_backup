from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import GreenBillUserCreationForm, GreenBillUserChangeForm
from .models import GreenBillUser, Merchant_users, UserProfileImage, MerchantProfile, PartnerProfile, Partner_users, PartnerUniqueIds, MerchantUniqueIds

class CustomUserAdmin(UserAdmin):
    add_form = GreenBillUserCreationForm
    form = GreenBillUserChangeForm
    model = GreenBillUser
    list_display = ('id','mobile_no', 'first_name', 'last_name', 'is_staff', 'is_merchant', 'c_dob', 'is_merchant_staff' ,'is_customer', 'is_partner', 'is_active', 'date_joined', 'c_unique_id', 'm_email', 'merchant_referral_code', 'customer_referral_code', 'c_used_referral_code', 'm_used_referral_code', 'm_unique_id', 'p_unique_id', 'email_verification_url','c_area')
    list_filter = ('mobile_no', 'is_staff', 'is_merchant', 'is_merchant_staff' ,'is_customer', 'is_partner', 'is_active', 'date_joined', 'c_unique_id', 'merchant_referral_code', 'customer_referral_code')
    fieldsets = (
        (None, {'fields': ('mobile_no', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_merchant', 'is_merchant_staff' ,'is_customer', 'is_partner', 'c_unique_id', 'merchant_referral_code', 'customer_referral_code', 'c_used_referral_code', 'm_used_referral_code', 'is_verified_email')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_no', 'password1', 'password2', 'is_staff', 'is_active', 'date_joined', 'is_merchant', 'is_merchant_staff' ,'is_customer', 'is_partner', 'c_unique_id', 'merchant_referral_code', 'customer_referral_code', 'c_used_referral_code', 'm_used_referral_code', 'is_verified_email')}
        ),
    )
    search_fields = ('mobile_no',)
    ordering = ('mobile_no',)


admin.site.register(GreenBillUser, CustomUserAdmin)
admin.site.register(Merchant_users)
admin.site.register(Partner_users)
admin.site.register(UserProfileImage)

class MerchantProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'm_user', 'm_business_name', 'm_business_category', 'm_active_account')
admin.site.register(MerchantProfile, MerchantProfileAdmin)


# class PartnerProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'p_user', 'p_business_name', 'p_business_category', 'p_active_account')
admin.site.register(PartnerProfile)

# admin.site.register(Partner_users)

admin.site.register(MerchantUniqueIds)
admin.site.register(PartnerUniqueIds)