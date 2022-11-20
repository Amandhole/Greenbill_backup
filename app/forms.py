# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import GreenBillUser, MerchantProfile
from category_and_tags.models import business_category
from .models import emailSetting, generalSetting

class ChangePasswordForm(UserCreationForm):
    password = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = GreenBillUser
        fields = ('password', 'password1', 'password2')

class ChangeMerchnatBusinessForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ChangeMerchnatBusinessForm, self).__init__(*args, **kwargs)
        self.fields['m_business_change'].queryset = MerchantProfile.objects.filter(m_user=user)
        self.fields['m_business_change'].initial = MerchantProfile.objects.get(m_user=user, m_active_account = True)

    m_business_change = forms.ModelChoiceField(required=True,
        widget=forms.Select(
            attrs={
                "placeholder" : "Select Business",                
                "class": "form-control",
                "onchange": "if(document.getElementById('id_m_business_change').value != ''){ this.form.submit() }"
            }
        ),
        queryset = None, 
        to_field_name="id",
        empty_label= None
    )

class EmailForm(forms.ModelForm):
    class Meta:
        model = emailSetting
        fields = "__all__"

class PasswordResetForm(forms.Form):
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={
                "placeholder" : "Mobile Number",                
                "class": "form-control",
                "value": "",
                "maxlength":10,
            }
    ), label="")

class generalSettingForm(forms.Form):
    user_id = forms.CharField(required=True)
    business_name = forms.CharField(required=False)
    business_code = forms.CharField(required=False)
    mobile_no = forms.CharField(required=False)
    alternate_mobile_number  = forms.CharField(required=False)
    email = forms.CharField(required=False)
    alternate_email  = forms.CharField(required=False)
    address  = forms.CharField(required=False)
    city   = forms.CharField(required=False)
    area   = forms.CharField(required=False)
    distrct  = forms.CharField(required=False)
    state   = forms.CharField(required=False)
    pin_code  = forms.CharField(required=False)
    pan_number = forms.CharField(required=False)
    aadhaar_number  = forms.CharField(required=False)
    gstin  = forms.CharField(required=False)
    cin  = forms.CharField(required=False)
    tin_vat_number  = forms.CharField(required=False)
    bank_account_number  = forms.CharField(required=False)
    bank_IFSC_code  = forms.CharField(required=False)
    bank_name  = forms.CharField(required=False)
    bank_branch  = forms.CharField(required=False)
    cancelled_cheque_certificate = forms.FileField(required=False)
    GSTIN_certificate = forms.FileField(required=False)
    CIN_certificate = forms.FileField(required=False)
    udyog_adhar_certificate  = forms.FileField(required=False)
    date_format = forms.CharField(required=False)
    currency = forms.CharField(required=False)
    android_app_url = forms.CharField(required=False)
    iphone_app_url = forms.CharField(required=False)
    o_business_logo = forms.ImageField(required=False)
    o_digital_signature = forms.ImageField(required=False)
    o_business_stamp = forms.ImageField(required=False)
    address_proof = forms.FileField(required=False)


class FileUploadForm(forms.Form):
    docfile = forms.FileField()


class stampuploadform(forms.Form):
    stampfile = forms.FileField()


class logouploadform(forms.Form):
    logofile = forms.FileField()
