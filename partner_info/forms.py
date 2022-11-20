from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import GreenBillUser, UserProfileImage
from .models import bulkMailSmsPartnerModel, PartnerdiasbleReasons



class partnerDisablereasonForm(forms.Form):
    p_disable_reason = forms.CharField

class bulkMailSmsPartnerForm(forms.ModelForm):
    class Meta:
        model = bulkMailSmsPartnerModel
        fields = ('message',)

class SoftwarePartnerSignUpForm1(UserCreationForm):
    mobile_no = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Mobile Number *",                
                "class": "form-control",
                "maxlength": 10,
            }
        ))
    p_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email *",                
                "class": "form-control"
            }
    ))
    password1 = forms.CharField(required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password *",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm Password *",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = GreenBillUser
        fields = ('mobile_no', 'p_email',)

class PartnerProfileEditForm(forms.Form):
    p_business_name = forms.CharField(required=False)
    p_business_category = forms.CharField(required=False)
    p_business_description = forms.CharField(required=False)
    p_pin_code = forms.CharField(required=False)
    p_city = forms.CharField(required=False)
    p_area = forms.CharField(required=False)
    p_district = forms.CharField(required=False)
    p_state = forms.CharField(required=False)
    p_address = forms.CharField(required=False)
    p_landline_number = forms.CharField(required=False)
    p_alternate_mobile_number = forms.CharField(required=False)
    p_company_email = forms.CharField(required=False)
    p_alternate_email = forms.CharField(required=False)
    p_pan_number = forms.CharField(required=False)
    p_gstin = forms.CharField(required=False)
    p_GSTIN_certificate = forms.FileField(required=False)
    p_cin = forms.CharField(required=False)
    p_CIN_certificate = forms.FileField(required=False)
    p_business_logo = forms.ImageField(required=False)
    p_business_stamp = forms.ImageField(required=False)
    p_digital_signature = forms.ImageField(required=False)
    p_bank_account_number = forms.CharField(required=False)
    p_bank_IFSC_code = forms.CharField(required=False)
    p_bank_name = forms.CharField(required=False)
    p_bank_branch = forms.CharField(required=False)
    p_category = forms.CharField(required=False)


