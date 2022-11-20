from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import GreenBillUser, UserProfileImage


class GreenBillUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = GreenBillUser
        fields = ('mobile_no',)

class GreenBillUserChangeForm(UserChangeForm):

    class Meta:
        model = GreenBillUser
        fields = ('mobile_no',)

class ProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=True)

class MerchantProfileForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    m_email = forms.CharField(required=True)
    m_designation = forms.CharField(required=False)
    m_adhaar_number = forms.CharField(required=False)
    m_pan_number = forms.CharField(required=False)
    m_dob = forms.DateField(required=False)
    m_area = forms.CharField(required=False)

class PartnerProfileForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    p_email = forms.CharField(required=True)
    p_designation = forms.CharField(required=False)
    p_adhaar_number = forms.CharField(required=False)
    p_pan_number = forms.CharField(required=False)
    p_dob = forms.DateField(required=False)

# class PartnerCategoryForm(forms.ModelForm):
#     categories = (
#         ('1', 'Software Partner'),
#         ('2', 'Marketing Partner'),
#     )
#     p_category = forms.ChoiceField(required=True, label="Partner Category",
#         widget=forms.Select(
#             attrs={ 
#                 "placeholder" : "Partner Category",                
#                 "class": "form-control"
#             }
#         ),
#         choices=categories,
#     )
#     class Meta:
#         model = PartnerCategory
#         fields = "__all__"
#         exclude = ['user']

class CustomerProfileForm(forms.Form):
    email = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    c_gender = forms.CharField(required=False)
    c_dob = forms.DateField(required=False)
    c_address_1 = forms.CharField(required=False)
    c_address_2 = forms.CharField(required=False)
    c_area = forms.CharField(required=False)
    c_state = forms.CharField(required=False)
    c_pincode = forms.CharField(required=False)
    c_city = forms.CharField(required=False)

class ImageForm(forms.ModelForm):
    class Meta:
        model = UserProfileImage
        fields = "__all__"
        exclude = ['user']


class UploadCropImageForm(forms.Form):
    profileimage = forms.FileField()


class merchantCropImageForm(forms.Form):
    merchantprofileimage = forms.FileField()


class customerCropImageForm(forms.Form):
    customerprofileimage = forms.FileField()


class partnerCropImageForm(forms.Form):
    partnerprofileimage = forms.FileField()
