from django import forms
from django.db import models
from django.db.models import fields
from .models import partnermodels
from users.models import PartnerProfile
from category_and_tags.models import business_category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import GreenBillUser, UserProfileImage



# class partnerforms(forms.Form):
#     my_partner = forms.CharField()



class PartnerBusinessForm(forms.ModelForm):
    p_business_name = forms.CharField(label="Business Name",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Business Name ",                
                "class": "form-control",
            }
        ))
    p_business_category = forms.ModelChoiceField(label="Business Category",
        widget=forms.Select(
            attrs={ 
                "placeholder" : "Business Category",                
                "class": "form-control"
            }
        ),
        queryset = business_category.objects.all(), 
        empty_label='Select Category'
    )
    p_city = forms.CharField(label="City",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "City",                
                "class": "form-control"
            }
    ))
    p_district = forms.CharField(label="District",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "District",                
                "class": "form-control"
            }
    ))
    p_state = forms.CharField(label="State",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "State",                
                "class": "form-control"
            }
    ))
    p_pin_code = forms.CharField(label="Pin Code",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Pin Code",                
                "class": "form-control"
            }
    ))
    p_area = forms.CharField(label="Area",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Area",                
                "class": "form-control"
            }
    ))
    p_landline_number = forms.CharField(label="Area",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Mobile Number",                
                "class": "form-control"
            }
    ))
    p_company_email = forms.EmailField(label="Area",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Email",                
                "class": "form-control"
            }
    ))
    class Meta:
        model = PartnerProfile
        fields = ('p_business_name', 'p_business_category', 'p_city', 'p_district', 'p_state', 'p_pin_code', 'p_area', 'p_landline_number', 'p_company_email')