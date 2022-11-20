# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import GreenBillUser, MerchantProfile, PartnerProfile
from category_and_tags.models import business_category


class LoginForm(forms.Form):
    mobile_no = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Mobile Number*",                
                "class": "form-control",
                "value": "",
                "maxlength":10,
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password*",                
                "class": "form-control",
                "value": "",
            }
        ))
    remember_me = forms.BooleanField(required=False, 
        widget=forms.CheckboxInput(
            attrs={
                "placeholder" : "Remember Me",
                "class" : "form-check-input"
            }
    ))

class SignUpForm(UserCreationForm):
    mobile_no = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Mobile Number*",                
                "class": "form-control",
                "maxlength":10,
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email*",                
                "class": "form-control",
                "id":"memail",
            }
        ))
    c_dob = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(2020, 1900, -1),
            attrs={
                "placeholder" : "DOB",                
                "class": "form-control"
            }
        ))
    c_state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "State",                
                "class": "form-control"
            }
        ))
    c_area = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder" : "Area*",                
                "class": "form-control",
                "rows": "1"
            }
        ))
    c_pin_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Pin Code*",                
                "class": "form-control",
                "maxlength": 6,
                "minlength": 6,
            }
        ))
    c_city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "City",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password*",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm Password*",                
                "class": "form-control"
            }
        ))
    c_used_referral_code = forms.CharField(required = False,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Referral Code",                
                "class": "form-control",
            }
        ))

    class Meta:
        model = GreenBillUser
        fields = ('mobile_no', 'email', 'c_dob', 'c_state','c_area', 'c_pin_code')


class MerchantSignUpForm(UserCreationForm):
    mobile_no = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Mobile Number *",                
                "class": "form-control",
                "maxlength":10,
            }
        ))
    m_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email *",                
                "class": "form-control"
            }
    ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password *",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm Password *",                
                "class": "form-control"
            }
    ))

    class Meta:
        model = GreenBillUser
        fields = ('mobile_no', 'm_email',)

class MerchantSignUpOtherDetailsForm(forms.Form):

    m_business_name = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Business Name *",                
                "class": "form-control",
                'maxlength': '50',
            }
        ))
    m_business_category = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={ 
                "placeholder" : "Mobile Number ",                
                "class": "form-control"
            }
        ),
        queryset = business_category.objects.order_by('business_category_name'), 
        empty_label='Select Business Category *'
    )
    m_city = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "City *",                
                "class": "form-control"
            }
    ))
    m_area = forms.CharField(
        widget=forms.Textarea(
            attrs={ 
                "placeholder" : "Area *",                
                "class": "form-control",
                "rows": "1"
            }
    ))
    m_district = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "District *",                
                "class": "form-control"
            }
    ))
    m_state = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "State *",                
                "class": "form-control"
            }
    ))
    m_pin_code = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Pin Code *",                
                "class": "form-control",
                "maxlength": 6,
                "minlength": 6,
            }
    ))
    m_used_referral_code = forms.CharField(required = False,
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Referral Code",                 
                "class": "form-control",
                'required': False
            }
    ))

    CHOICES=[('Loyalty Point','Loyalty point'),
         ('Membership','Membership'),
         ('Bothplan','Bothplan')]

    loyalty_point = forms.ChoiceField( choices=CHOICES,
        widget=forms.RadioSelect(
            attrs={
            "class":"form-control",
            }
    ))

    # m_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             "placeholder" : "Address",                
    #             "class": "form-control",
    #             "rows": "2"
    #         }
    # ))

    class Meta:
        model = MerchantProfile
        fields = ('m_business_name', 'm_business_category', 'm_city', 'm_area', 'm_district', 'm_state', 'm_pin_code','loyalty_point')


class SoftwarePartnerSignUpForm(UserCreationForm):
    mobile_no = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Mobile Number *",                
                "class": "form-control",
                "maxlength":10,
            }
        ))
    p_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email *",                
                "class": "form-control"
            }
    ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password *",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm Password *",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = GreenBillUser
        fields = ('mobile_no', 'p_email',)


class SoftwarePartnerOtherDetailsForm(forms.Form):
    categories = (
        ('Software Partner', 'Software Partner'),
        ('Marketing Partner', 'Marketing Partner'),
    )
    p_business_name = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Business Name *",                
                "class": "form-control"
            }
        ))
    p_business_category = forms.ModelChoiceField(required=False,
        widget=forms.Select(
            attrs={ 
                "placeholder" : "Mobile Number",                
                "class": "form-control"
            }
        ),
        queryset = business_category.objects.all(), 
        empty_label='Select Business Category *'
    )
    p_business_description = forms.CharField(
        widget=forms.Textarea(
            attrs={ 
                "placeholder" : "Business Description *",                
                "class": "form-control",
                "rows": "1"
            }
    ))
    p_city = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "City *",                
                "class": "form-control"
            }
    ))
    p_district = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "District *",                
                "class": "form-control"
            }
    ))
    p_state = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "State *",                
                "class": "form-control"
            }
    ))
    p_pin_code = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Pin Code *",                
                "class": "form-control",
                "maxlength":6,
                "minlength":6,
            }
    ))
    CHOICES=[('Loyalty Point','Loyalty point'),
         ('Membership','Membership'),
         ('Bothplan','Bothplan')]

    loyalty_point = forms.ChoiceField( choices=CHOICES,
        widget=forms.RadioSelect(
            attrs={
            "class":"form-control",
            }
    ))
    # membership = forms.ChoiceField(
    #     widget=forms.RadioSelect(
    #         attrs={
    #         "class":"form-control",
    #         }
    # ))
    # bothplan = forms.ChoiceField(
    #     widget=forms.RadioSelect(
    #         attrs={
    #         "class":"form-control",
    #         }
    # ))
    # p_commission_per_bill = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={ 
    #             "placeholder" : "Commission / Bill *",                
    #             "class": "form-control"
    #         }
    #     )
    # )
    class Meta:
        model = PartnerProfile
        fields = ('p_business_name', 'p_business_category', 'business_description', 'p_city', 'p_district', 'p_state', 'p_pin_code','loyalty_point',)

class SoftwareCommisionDetailsForm(forms.Form):
    merchant_commission = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Commission/Subscription % *",                
                "class": "form-control",
                'required': False,
                "maxlength":2,
                "minlength":1,
            }
        )
    )
    class Meta:
        model = PartnerProfile
        fields = ('merchant_commission')

class SoftwarePartnerCommisionPerBillsDetailsForm(forms.Form):
    p_commission_per_bill = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Cost/Digital Delivery*",                
                "class": "form-control",
            }
        )
    )
    p_cost_per_sms = forms.CharField(
        widget=forms.TextInput(
            attrs={
                  "placeholder":"Cost/SMS*",
                  "class":"form-control",
            }
        )
    )

    class Meta:
        model = PartnerProfile
        fields = ('p_commission_per_bill')

class MarketingPartnerCommisionDetailsForm(forms.Form):
    p_commission_per_sms_bill = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Commission / SMS Bill *",                
                "class": "form-control"
            }
        )
    )
    p_commission_per_digital_bill = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Commission / Digital Bill *",                
                "class": "form-control"

            }
        )
    )
    p_commission_per_other_services = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "placeholder": "Commission/Other Services*",
                "class": "form-control",
                "maxlength":2,
                "minlength":1,
            }
        )    
    )
    class Meta:
        model = PartnerProfile
        fields = ('p_commission_per_sms_bill','p_commission_per_digital_bill')
