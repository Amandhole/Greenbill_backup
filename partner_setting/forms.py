"""
Copyright (c) 2020 - present Hind Softwares
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
User = settings.AUTH_USER_MODEL

class PartnergeneralSettingForm(forms.Form):
    partner_setting_id = forms.CharField(required=True)
    business_name = forms.CharField(required=True)
    business_category = forms.CharField(required=False)
    pin_code = forms.CharField(required=False)
    city = forms.CharField(required=False)
    area = forms.CharField(required=False)
    district = forms.CharField(required=False)
    state = forms.CharField(required=False)
    address = forms.CharField(required=False)
    landline_number = forms.CharField(required=False)
    alternate_mobile_number = forms.CharField(required=False)
    company_email = forms.CharField(required=False)
    alternate_email = forms.CharField(required=False)
    pan_number = forms.CharField(required=False)
    aadhaar_number = forms.CharField(required=False)
    gstin = forms.CharField(required=False)
    GSTIN_certificate = forms.FileField(required=False)
    address_proof = forms.FileField(required=False)
    udyog_adhar_certificate = forms.FileField(required=False)
    cancelled_cheque_certificate = forms.FileField(required=False)
    cin = forms.CharField(required=False)
    tin_vat_number = forms.CharField(required=False)
    CIN_certificate = forms.FileField(required=False)
    profile_image = forms.ImageField(required=False)
    business_logo = forms.ImageField(required=False)
    business_stamp = forms.ImageField(required=False)
    digital_signature = forms.ImageField(required=False)
    bank_account_number = forms.CharField(required=False)
    bank_IFSC_code = forms.CharField(required=False)
    bank_name = forms.CharField(required=False)
    bank_branch = forms.CharField(required=False)
    p_website_url = forms.CharField(required=False)
    p_business_name_for_billing = forms.CharField(required=False)
    p_commission_per_bill = forms.CharField(required=False)
    p_billing_phone = forms.CharField(required=False)
    p_billing_address = forms.CharField(required=False)
    p_billing_email = forms.CharField(required=False)
    p_bank_account_entity = forms.CharField(required=False)
    p_adress_account_entity = forms.CharField(required=False)
    p_pan_legal_entity = forms.ImageField(required=False)
    p_signature_proof = forms.ImageField(required=False)
    p_company_registration_certificate = forms.ImageField(required=False)
    p_payu_schedule_upload  = forms.ImageField(required=False)


class partneruploadlogoForm(forms.Form):
    partnerlogofile = forms.FileField()


class partneruploadstampForm(forms.Form):
    partnerstampfile = forms.FileField()


class partneruploadsignatureForm(forms.Form):
    partnersignaturefile = forms.FileField()


class PaymentSettingForm(forms.Form):
    payu_key = forms.CharField(required=True)
    payu_salt = forms.CharField(required=True)



class PartnerSmsSettingForm(forms.Form):
    user_id = forms.CharField(required=True)
    sms_header = forms.CharField(required=True)
    status = forms.CharField(required=True)


class MarketingPartnergeneralSettingForm(forms.Form):
    partner_setting_id = forms.CharField(required=True)
    business_name = forms.CharField(required=True)
    pin_code = forms.CharField(required=False)
    city = forms.CharField(required=False)
    area = forms.CharField(required=False)
    district = forms.CharField(required=False)
    state = forms.CharField(required=False)
    address = forms.CharField(required=False)
    landline_number = forms.CharField(required=False)
    alternate_mobile_number = forms.CharField(required=False)
    company_email = forms.CharField(required=False)
    alternate_email = forms.CharField(required=False)
    pan_number = forms.CharField(required=False)
    aadhaar_number = forms.CharField(required=False)
    gstin = forms.CharField(required=False)
    GSTIN_certificate = forms.FileField(required=False)
    address_proof = forms.FileField(required=False)
    udyog_adhar_certificate = forms.FileField(required=False)
    cancelled_cheque_certificate = forms.FileField(required=False)
    cin = forms.CharField(required=False)
    tin_vat_number = forms.CharField(required=False)
    CIN_certificate = forms.FileField(required=False)
    profile_image = forms.ImageField(required=False)
    business_logo = forms.ImageField(required=False)
    business_stamp = forms.ImageField(required=False)
    digital_signature = forms.ImageField(required=False)
    bank_account_number = forms.CharField(required=False)
    bank_IFSC_code = forms.CharField(required=False)
    bank_name = forms.CharField(required=False)
    bank_branch = forms.CharField(required=False)
    p_commission_per_sms_bill = forms.CharField(required=False)
    p_commission_per_digital_bill = forms.CharField(required=False)
    merchant_commission = forms.CharField(required=False)


