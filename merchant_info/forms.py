from django import forms
from users.models import MerchantProfile
from category_and_tags.models import business_category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import GreenBillUser, UserProfileImage
from .models import bulkMailSmsMerchantModel


class merchantDisablereasonForm(forms.Form):
    m_disable_reason = forms.CharField()


class bulkMailSmsMerchantForm(forms.ModelForm):
    class Meta:
        model = bulkMailSmsMerchantModel
        fields = ('message',)

class merchantBusinessesForm(forms.ModelForm):
    m_business_name = forms.CharField(label="Business Name",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Business Name ",                
                "class": "form-control",
            }
        ))
    m_business_category = forms.ModelChoiceField(label="Business Category",
        widget=forms.Select(
            attrs={ 
                "placeholder" : "Business Category",                
                "class": "form-control"
                
            }
        ),
        queryset = business_category.objects.all().order_by('business_category_name'), 
        empty_label='Select Category'
    )
    m_city = forms.CharField(label="City",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "City",                
                "class": "form-control"
            }
    ))
    m_district = forms.CharField(label="District",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "District",                
                "class": "form-control",
                "id":'district',
            }
    ))
    m_state = forms.CharField(label="State",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "State",                
                "class": "form-control"
            }
    ))
    m_pin_code = forms.CharField(label="Pin Code",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Pin Code",                
                "class": "form-control",
                "maxlength":6,
                "minlength":6,
            }
    ))
    m_area = forms.CharField(label="Area",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Area",                
                "class": "form-control"
            }
    ))
    m_landline_number = forms.CharField(label="Mobile Number",
    widget=forms.TextInput(
        attrs={
            "placeholder" : " Mobile Number",
            "class" : "form-control",
        }
    ))
    m_address = forms.CharField(label="Address",
    widget=forms.TextInput(
        attrs={
            "placeholder" : "Address",
            "class" : "form-control",
        }
    ))
    class Meta:
        model = MerchantProfile
        fields = ('m_business_name', 'm_business_category', 'm_city', 'm_district', 
        'm_state', 'm_pin_code', 'm_area','m_landline_number','m_address')



class merchantBusinessesBranchForm(forms.ModelForm):
    m_business_name = forms.CharField(label="Business Branch Name",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Business Branch Name ",                
                "class": "form-control",
            }
        ))
    m_business_category = forms.ModelChoiceField(label="Business Branch Category",
        widget=forms.Select(
            attrs={ 
                "placeholder" : 'Business Branch Category', #"{{m_business_category_name}}",                
                "class": "form-control"
            }
        ),
        queryset = business_category.objects.all(), 
        empty_label='Select Category'
    )
    m_city = forms.CharField(label="City",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "City",                
                "class": "form-control"
            }
    ))
    m_district = forms.CharField(label="District",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "District",                
                "class": "form-control",
            }
    ))
    m_state = forms.CharField(label="State",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "State",                
                "class": "form-control"
            }
    ))
    m_pin_code = forms.CharField(label="Pin Code",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Pin Code",                
                "class": "form-control",
                "maxlength":6,
                "minlength":6,
            }
    ))
    m_area = forms.CharField(label="Area",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Area",                
                "class": "form-control"
            }
    ))
    m_landline_number = forms.CharField(label="Mobile Number",
    widget=forms.TextInput(
        attrs={
            "placeholder" : " Mobile Number",
            "class" : "form-control",
        }
    ))
    m_address = forms.CharField(label="Address",
    widget=forms.TextInput(
        attrs={
            "placeholder" : "Address",
            "class" : "form-control",
        }
    )
    )
    class Meta:
        model = MerchantProfile
        fields = ('m_business_name', 'm_business_category',
         'm_city', 'm_district', 'm_state', 'm_pin_code',
         'm_area','m_landline_number','m_address')



# class merchantEditBusinessesForm_1(forms.ModelForm):
#     m_business_name = forms.CharField(label="Business Name",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Business Name ",                
#                 "class": "form-control",
#             }
#         ))
#     m_business_category = forms.ModelChoiceField(label="Business Category",
#         widget=forms.Select(
#             attrs={ 
#                 "placeholder" : "Business Category",                
#                 "class": "form-control"
#             }
#         ),
#         queryset = business_category.objects.all(), 
#         empty_label='Select Business Category'
#     )
#     m_city = forms.CharField(label="City",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "City",                
#                 "class": "form-control"
#             }
#     ))
#     m_district = forms.CharField(label="District",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "District",                
#                 "class": "form-control"
#             }
#     ))
#     m_state = forms.CharField(label="State",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "State",                
#                 "class": "form-control"
#             }
#     ))
#     m_pin_code = forms.CharField(label="Pin Code",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Pin Code",                
#                 "class": "form-control"
#             }
#     ))
#     m_area = forms.CharField(label="Area",
#         widget=forms.Textarea(
#             attrs={ 
#                 "placeholder" : "Area",                
#                 "class": "form-control",
#                 'rows': "1"
#             }
#     ))
#     m_address = forms.CharField(label="Address",
#         widget=forms.Textarea(
#             attrs={ 
#                 "placeholder" : "Address",                
#                 "class": "form-control",
#                 'rows': "1"
#             }
#     ))
#     m_landline_number = forms.CharField(required=False, label="Landline Number",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Landline Number",                
#                 "class": "form-control"
#             }
#     ))
#     m_alternate_mobile_number = forms.CharField(required=False, label="Alternate Mobile Number",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Alternate Mobile Number",                
#                 "class": "form-control"
#             }
#     ))
#     m_company_email = forms.CharField(label="Company Email",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Company Email",                
#                 "class": "form-control"
#             }
#     ))
#     m_alternate_email = forms.CharField(required=False, label="Alternate Email",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Alternate Email",                
#                 "class": "form-control"
#             }
#     ))
#     m_pan_number = forms.CharField(label="Pan Number",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Pan Number",                
#                 "class": "form-control"
#             }
#     ))
#     m_gstin = forms.CharField(required=False, label="GSTIN",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "GSTIN",                
#                 "class": "form-control"
#             }
#     ))
#     m_cin = forms.CharField(required=False, label="CIN",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "CIN",                
#                 "class": "form-control"
#             }
#     ))
#     m_bank_account_number = forms.CharField(label="Bank Account Number",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Bank Account Number",                
#                 "class": "form-control"
#             }
#     ))
#     m_bank_IFSC_code = forms.CharField(label="Bank IFSC Code",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Bank IFSC Code",                
#                 "class": "form-control"
#             }
#     ))
#     m_bank_name = forms.CharField(label="Bank Name",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Bank Name",                
#                 "class": "form-control"
#             }
#     ))
#     m_bank_branch = forms.CharField(label="Bank Branch",
#         widget=forms.TextInput(
#             attrs={ 
#                 "placeholder" : "Bank Branch",                
#                 "class": "form-control"
#             }
#     ))
#     m_GSTIN_certificate = forms.FileField(required=False, label="GSTIN Certificate")
#     m_CIN_certificate = forms.FileField(required=False, label="CIN Certificate")
#     m_business_logo = forms.ImageField(required=False, label="Business Logo")
#     m_business_stamp = forms.ImageField(required=False, label="Business Stamp")
#     m_digital_signature = forms.ImageField(required=False, label="Digital Signature")
    

#     class Meta:
#         model = MerchantProfile
#         fields = '__all__'
#         exclude = ('m_user', 'm_active_account', )


class MerchantSignUpForm1(UserCreationForm):
    mobile_no = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Mobile Number *",                
                "class": "form-control"
            }
        ))
    m_email = forms.EmailField(
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
        fields = ('mobile_no', 'm_email',)


class merchantEditBusinessesForm(forms.Form):
    m_business_name = forms.CharField(required=False)
    m_business_category = forms.CharField(required=False)
    m_pin_code = forms.CharField(required=False)
    m_city = forms.CharField(required=False)
    m_area = forms.CharField(required=False)
    m_district = forms.CharField(required=False)
    m_state = forms.CharField(required=False)
    m_address = forms.CharField(required=False)
    m_landline_number = forms.CharField(required=False)
    m_alternate_mobile_number = forms.CharField(required=False)
    m_company_email = forms.CharField(required=False)
    m_alternate_email = forms.CharField(required=False)
    m_pan_number = forms.CharField(required=False)
    m_gstin = forms.CharField(required=False)
    m_GSTIN_certificate = forms.FileField(required=False)
    m_cin = forms.CharField(required=False)
    m_CIN_certificate = forms.FileField(required=False)
    m_business_logo = forms.ImageField(required=False)
    m_business_stamp = forms.ImageField(required=False)
    m_digital_signature = forms.ImageField(required=False)
    m_bank_account_number = forms.CharField(required=False)
    m_bank_IFSC_code = forms.CharField(required=False)
    m_bank_name = forms.CharField(required=False)
    m_bank_branch = forms.CharField(required=False)
    m_address_bank_account = forms.ImageField(required=False)
    m_bank_account_entry = forms.ImageField(required=False)
    bank_account_entity_m1 = forms.CharField(required=False)
    bank_account_entity_adress2 = forms.CharField(required=False)
    schedule_pdf_upload = forms.FileField(required=False)
