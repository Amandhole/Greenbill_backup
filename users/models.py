from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import GreenBillUserManager

from category_and_tags.models import business_category

class GreenBillUser(AbstractBaseUser, PermissionsMixin):
    mobile_no = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=200, blank= True, default='')
    last_name = models.CharField(max_length=200, blank= True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_merchant_staff = models.BooleanField(default=False)

    # For Customer
    c_email = models.EmailField(blank= True, default='')
    c_dob = models.DateField(blank=True, null=True)
    c_gender = models.CharField(max_length=10, null=True)
    c_address_1 = models.CharField(max_length=200, default='', null=True)
    c_address_2 = models.CharField(max_length=200, default='', null=True)
    c_state = models.CharField(max_length=100, default='', null=True)
    c_area = models.CharField(max_length=500, default='', null=True)
    c_pincode = models.CharField(max_length=100, default='', null=True)
    c_city = models.CharField(max_length=200, default='', null=True)
    c_unique_id = models.CharField(max_length=6, default='', null=True, blank= True)
    
    # For Merchant
    m_email = models.EmailField(blank= True, default='')
    m_designation = models.CharField(max_length=100, default='')
    m_adhaar_number = models.CharField(max_length=100, default='')
    m_pan_number = models.CharField(max_length=100, default='')
    m_dob = models.DateField(blank=True, null=True)

    # For Software Partner
    p_email = models.EmailField(blank= True, default='')
    p_designation = models.CharField(max_length=100, default='')
    p_adhaar_number = models.CharField(max_length=100, default='')
    p_pan_number = models.CharField(max_length=100, default='')
    p_dob = models.DateField(blank=True, null=True)
    
    date_joined = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=50, default='', null=True, blank= True)
    disable_reason = models.CharField(max_length=200, blank=True, null=True)
    disable_date = models.DateTimeField(blank=True, null=True)

    merchant_referral_code = models.CharField(max_length=50, default='', null=True, blank= True)
    customer_referral_code = models.CharField(max_length=50, default='', null=True, blank= True)

    c_used_referral_code = models.CharField(max_length=500, default='', null=True, blank= True)
    m_used_referral_code = models.CharField(max_length=500, default='', null=True, blank= True)

    m_unique_id = models.CharField(max_length=100, default='', null=True, blank= True)
    p_unique_id = models.CharField(max_length=100, default='', null=True, blank= True)

    email_verification_url = models.CharField(max_length=50, default='', null=True, blank= True)
    is_verified_email = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile_no'
    REQUIRED_FIELDS = []

    objects = GreenBillUserManager()

    def __str__(self):
        return self.mobile_no

class MerchantUniqueIds(models.Model):
    m_unique_no = models.CharField(max_length=100, default='', null=True, blank= True)

class PartnerUniqueIds(models.Model):
    p_unique_no = models.CharField(max_length=100, default='', null=True, blank= True)

class UserProfileImage(models.Model):     
    user   = models.OneToOneField(GreenBillUser, null=True, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_pic', default="")
    c_profile_image = models.ImageField(null=True, blank=True, upload_to='profile_pic', default="")
    m_profile_image = models.ImageField(null=True, blank=True, upload_to='profile_pic', default="")
    p_profile_image = models.ImageField(null=True, blank=True, upload_to='profile_pic', default="")

class MerchantProfile(models.Model):
    m_user = models.ForeignKey(GreenBillUser,related_name="merchant_record", null=True, on_delete=models.CASCADE)
    m_business_name = models.CharField(max_length=500, default='')
    merchant_by_partner = models.ForeignKey(GreenBillUser, related_name="partner_record", null=True, on_delete=models.CASCADE, blank = True)
    m_business_category = models.ForeignKey(business_category, null=True, on_delete = models.SET_NULL)
    m_pin_code = models.CharField(max_length=20, default='')
    m_city = models.CharField(max_length=500, default='')
    m_area = models.CharField(max_length=500, default='', null=True)
    m_district = models.CharField(max_length=500, default='')
    m_state = models.CharField(max_length=500, default='')
    m_address = models.CharField(max_length=1000, default='')
    m_landline_number = models.CharField(max_length=20, default='')
    m_alternate_mobile_number = models.CharField(max_length=20, default='')
    m_company_email = models.EmailField(blank= True, default='')
    m_alternate_email = models.EmailField(blank= True, default='')
    m_pan_number = models.CharField(max_length=10, default='')
    m_aadhaar_number = models.CharField(max_length=50, default='')
    m_gstin = models.CharField(max_length=100, default='')
    m_GSTIN_certificate = models.FileField(null=True, blank=True, upload_to='merchant_GSTIN_certificate', default="")
    m_PAN_card = models.FileField(null=True, blank=True, upload_to='merchant_PAN_card', default="")
    m_cin = models.CharField(max_length=100, default='')
    m_CIN_certificate = models.FileField(null=True, blank=True, upload_to='merchant_CIN_certificate', default="")
    m_bank_account_number = models.CharField(max_length=100, default='')
    m_bank_IFSC_code = models.CharField(max_length=100, default='')
    m_bank_name = models.CharField(max_length=500, default='')
    m_bank_branch = models.CharField(max_length=500, default='')
    Name_Entity_Account = models.CharField(max_length=500, default='')
    Address_Entity_Bank_Account = models.CharField(max_length=500, default='')
    Entity_Account_m = models.CharField(max_length=500, default='')
    Entity_Bank_Account_m = models.CharField(max_length=500, default='')
    # schedule_pdf_upload = models.ImageField(null=True,blank=True, upload_to='payu_schedule_upload_pdf', default="")
    
    schedule_pdf_upload = models.ImageField(null=True, blank=True, upload_to='merchant_business_logo', default="")

    m_digital_signature = models.ImageField(null=True, blank=True, upload_to='merchant_digital_signature', default="")
    m_business_logo = models.ImageField(null=True, blank=True, upload_to='merchant_business_logo', default="")
    m_business_stamp = models.ImageField(null=True, blank=True, upload_to='merchant_business_stamp', default="")
    m_cancel_bank_cheque_photo = models.ImageField(null=True, blank=True, upload_to='cancel_bank_cheque_photo', default="")
    m_other_document_certificate1 = models.ImageField(null=True, blank=True, upload_to='other_document_certificate1', default="")
    m_other_document_certificate2 = models.ImageField(null=True, blank=True, upload_to='other_document_certificate2', default="")
    m_bank_account_entry = models.ImageField(null=True, blank=True, upload_to='merchant_bank_aacount_entity', default="")
    company_registration_certificate = models.ImageField(null=True, blank=True, upload_to='merchant_registration_certificate', default="")
    m_address_bank_account = models.ImageField(null=True, blank=True, upload_to='merchant_adress_bank_acount', default="")
    m_other_document1 = models.CharField(max_length=500, default='',null=True)
    m_other_document2 = models.CharField(max_length=500, default='',null=True)
    address_proof =  models.FileField(null=True,blank=True, upload_to='merchant_address_proof', default="")
    merchant_authorised_sign = models.CharField(max_length=500, default='',null=True)
    m_active_account = models.BooleanField(default=False)
    m_vat_tin_number = models.CharField(max_length=100, default='')
    m_disabled_account = models.BooleanField(default=True)

    subscription_count = models.IntegerField(default=0)
    # def __str__(self):
    #     return u'{0}'.format(self.m_business_name)
    m_latest_account = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
     # status = 1 Approved
    # status = 0 Waiting for Approval
    # status = 2 Disapproved
    status = models.CharField(max_length=10, blank=True, null=True, default=0)
    disapprove_reason = models.CharField(max_length=120, null=True,blank=True)

    disable_reason = models.CharField(max_length=200, blank=True, null=True)
    by_partner = models.CharField(max_length=200, blank=True, null=True)

    m_website_url = models.CharField(max_length=200, blank=True, default='')

    m_unique_id = models.CharField(max_length=100, default='', null=True, blank= True)

    m_business_name_for_billing = models.CharField(max_length=100, default='', null=True, blank= True)

    m_billing_phone = models.CharField(max_length=100, default='', null=True, blank= True)

    m_billing_email = models.CharField(max_length=100, default='', null=True, blank= True)

    m_billing_address = models.CharField(max_length=100, default='', null=True, blank= True)

    loyalty_point = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.m_business_name + " (" + self.m_area + ")"


class PartnerProfile(models.Model):
    categories = (
        ('Software Partner', 'Software Partner'),
        ('Marketing Partner', 'Marketing Partner'),
    )
    p_user   = models.ForeignKey(GreenBillUser, null=True, on_delete=models.SET_NULL)
    p_category = models.CharField(max_length=100, null=True, choices=categories)
    p_business_name = models.CharField(max_length=500, default='')
    # p_business_category = models.CharField(max_length=100, null=True, blank=True, default='')
    p_business_description = models.CharField(max_length=500, null=True, blank=True)
    p_business_category = models.ForeignKey(business_category, null=True, blank=True, on_delete = models.SET_NULL)
    p_commission_per_bill = models.CharField(max_length=100, blank=True, null=True)
    merchant_commission = models.CharField(max_length=100, blank=True, null=True)
    p_pin_code = models.CharField(max_length=20, default='')
    p_city = models.CharField(max_length=500, default='')
    p_area = models.CharField(max_length=50,default='')
    p_district = models.CharField(max_length=500, default='')
    p_state = models.CharField(max_length=500, default='')
    p_address = models.CharField(max_length=1000, default='')
    p_landline_number = models.CharField(max_length=20, default='')
    p_alternate_mobile_number = models.CharField(max_length=20, default='')
    p_company_email = models.EmailField(blank= True, default='')
    p_alternate_email = models.EmailField(blank= True, default='')
    p_pan_number = models.CharField(max_length=50, default='')
    p_gstin = models.CharField(max_length=100, default='')
    p_GSTIN_certificate = models.FileField(null=True, blank=True, upload_to='partner_GSTIN_certificate', default="")
    p_cin = models.CharField(max_length=100, default='')
    p_CIN_certificate = models.FileField(null=True, blank=True, upload_to='partner_CIN_certificate', default="")
    p_bank_account_number = models.CharField(max_length=100, default='')
    p_bank_IFSC_code = models.CharField(max_length=100, default='')
    p_bank_name = models.CharField(max_length=500, default='')
    p_bank_branch = models.CharField(max_length=500, default='')
    p_digital_signature = models.ImageField(null=True, blank=True, upload_to='partner_digital_signature', default="")
    p_business_logo = models.ImageField(null=True, blank=True, upload_to='partner_business_logo', default="")
    p_business_stamp = models.ImageField(null=True, blank=True, upload_to='partner_business_stamp', default="")

    p_pan_legal_entity = models.ImageField(null=True, blank=True, upload_to='partner_legal_entity', default="")
    p_signature_proof = models.ImageField(null=True, blank=True, upload_to='partner_signature_proof', default="")
    p_company_registration_certificate = models.ImageField(null=True, blank=True, upload_to='partner_company_registration_certificate', default="")
    p_payu_schedule_upload = models.ImageField(null=True, blank=True, upload_to='partner_payu_upload', default="")
    
    p_aadhaar_number = models.CharField(max_length=50, default='')
    p_vat_tin_number = models.CharField(max_length=100, default='')
    p_active_account = models.BooleanField(default=True)
    p_cancelled_cheque_certificate = models.ImageField(null=True, blank=True, upload_to='cancel_bank_cheque_photo', default="")
    p_udyog_adhar_certificate = models.ImageField(null=True, blank=True, upload_to='other_document_certificate1', default="")
    address_proof =  models.FileField(null=True,blank=True, upload_to='address_proof', default="")

    p_billing_phone = models.CharField(max_length=100, default='', null=True, blank= True)
    p_billing_address = models.CharField(max_length=100, default='', null=True, blank= True)
    p_billing_email = models.CharField(max_length=100, default='', null=True, blank= True)


    # p_latest_account = models.BooleanField(default=False)
    p_disabled_account = models.BooleanField(default=True)
    status = models.CharField(max_length=10, blank=True, null=True, default=0)
    disapprove_reason = models.CharField(max_length=120, null=True,blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    disable_reason = models.CharField(max_length=200, blank=True, null=True)
    p_website_url = models.CharField(max_length=200, blank=True, default='')
    p_commission_per_sms_bill = models.CharField(max_length=100, blank=True, null=True)
    p_commission_per_digital_bill = models.CharField(max_length=100, blank=True, null=True)
    p_commission_per_other_services = models.CharField(max_length=100, blank=True, null=True, default = "0")
    p_business_name_for_billing = models.CharField(max_length=100, default='', null=True, blank= True)
    p_bank_account_entity = models.CharField(max_length=500, default='')
    p_adress_account_entity = models.CharField(max_length=500, default='')

    #loyalty Point
    loyalty_point = models.CharField(blank=True, null=True, max_length=100)
    membership = models.CharField(blank=True, null=True, max_length=100)
    bothplan = models.CharField(blank=True, null=True, max_length=100)


    def __str__(self):
        return self.p_business_name

class Merchant_users(models.Model):
    user_id = models.OneToOneField(GreenBillUser, null=True, on_delete=models.CASCADE)
    merchant_user_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.SET_NULL, related_name='+')
    raw_password = models.CharField(max_length=100, blank=True, null=True, default='')
    m_business_id = models.CharField(max_length=100, blank=True, null=True, default='')
    m_business_name = models.CharField(max_length=200, blank=True, null=True, default='')

class Partner_users(models.Model):
    user_id = models.OneToOneField(GreenBillUser, null=True, on_delete=models.CASCADE)
    partner_user_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.SET_NULL, related_name='+')
    raw_password = models.CharField(max_length=100, blank=True, null=True, default='')
    p_business_id = models.CharField(max_length=100, blank=True, null=True, default='')
    # p_user_id = models.CharField(max_length=100, blank=True, null=True, default='')
    p_business_name = models.CharField(max_length=200, blank=True, null=True, default='')

class UserslogDetails(models.Model):
    mobile_no = models.CharField(max_length=100, blank=True, null=True, default='')
    module_name = models.CharField(max_length=100, blank=True, null=True, default='')
    action = models.CharField(max_length=100, blank=True, null=True, default='')
    created_date = models.DateTimeField(default=timezone.now)
