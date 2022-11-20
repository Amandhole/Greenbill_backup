"""
Copyright (c) 2020 - present Hind Softwares
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
User = settings.AUTH_USER_MODEL
from .models import *

class MerchnatgeneralSettingForm(forms.Form):
    merchant_setting_id = forms.CharField(required=True)
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
    company_email = forms.CharField(max_length=100, required=False)
    alternate_email = forms.CharField(max_length=100, required=False)
    aadhaar = forms.CharField(required=False)
    pan_number = forms.CharField(required=False)
    gstin = forms.CharField(required=False)
    GSTIN_certificate = forms.FileField(required=False)
    #PAN_card = forms.FileField(required=True)
    cin = forms.CharField(required=False)
    CIN_certificate = forms.FileField(required=False)
    profile_image = forms.ImageField(required=False)
    business_logo = forms.ImageField(required=False)
    business_stamp = forms.ImageField(required=False)
    digital_signature = forms.ImageField(required=False)
    bank_account_number = forms.CharField(required=False)
    bank_IFSC_code = forms.CharField(required=False)
    bank_name = forms.CharField(required=False)
    bank_branch = forms.CharField(required=False)
    tin_vat_number = forms.CharField(required=False)
    cancelled_cheque_certificate = forms.FileField(required=False)
    udyog_adhar_certificate = forms.FileField(required=False)
    address_proof = forms.FileField(required=False)
    other_document1 = forms.CharField(required=False)
    other_document2 = forms.CharField(required=False)
    other_document_certificate1 = forms.ImageField(required=False)
    other_document_certificate2 = forms.ImageField(required=False)
    m_address_bank_account = forms.ImageField(required=False)
    m_bank_account_entry = forms.ImageField(required=False)
    bank_account_entity_m1 = forms.CharField(required=False)
    bank_account_entity_adress2 = forms.CharField(required=False)
    schedule_pdf_upload = forms.FileField(required=False)
    m_website_url = forms.CharField(required=False)
    m_business_name_for_billing = forms.CharField(required=False)
    m_billing_phone = forms.CharField(required=False)
    m_billing_email = forms.CharField(max_length=100, required=False)
    m_billing_address = forms.CharField(required=False)
    company_registration_certificate = forms.ImageField(required=False)




class CreateMerchantUserForm(forms.Form): 
    mobile_no = forms.CharField(required=True)
    email = forms.EmailField(max_length=100, required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    role_name = forms.CharField(required=False)

class UpdateMerchantUserForm(forms.Form): 
    edit_mobile_no = forms.CharField()
    edit_email = forms.EmailField(max_length=100)
    edit_first_name = forms.CharField()
    edit_last_name = forms.CharField()
    edit_role_name = forms.CharField()
    user_id = forms.CharField()

class MerchantEmailSettingForm(forms.Form):
    from_name = forms.CharField(required=True)
    from_email = forms.EmailField(max_length=100, required=True)
    footer = forms.CharField(required=False)
    signature = forms.CharField(required=False)

class MerchantSmsSettingForm(forms.Form):
    user_id = forms.CharField(required=True)
    sms_header = forms.CharField(required=True)
    status = forms.CharField(required=True)

class MerchantPetrolPumpProductForm(forms.ModelForm):
    # product_id = forms.CharField(label="Product Id",
    #     widget=forms.TextInput(
    #         attrs={ 
    #             "placeholder" : "Product Id",                
    #             "class": "form-control",
    #         }
    #     )
    # )
    product_name = forms.CharField(label="Product Name",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Product Name",                
                "class": "form-control",
            }
        )
    )
    product_cost = forms.CharField(label="Product Cost / Litre",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Product Cost / Litre",                
                "class": "form-control"
            }
        )
    )
    product_availability = forms.ChoiceField(label="Product Availability",
        widget=forms.Select(
            attrs={ 
                "placeholder" : "Product Availability",                
                "class": "form-control"
            }
        ),
        choices=(
        ('', 'Select Product Availability'),
        ('Yes', 'Yes'),
        ('No', 'No')
        ),
    )
    class Meta:
        model = MerchantPetrolPump
        fields = "__all__"
        exclude = ['user']


vehicle_type_choices= [
    ('','Select Vehicle Type'),
    ('2 - Wheeler', '2 - Wheeler'),
    ('3 - Wheeler', '3 - Wheeler'),
    ('4 - Wheeler', '4 - Wheeler'),
    ('Lorry', 'Lorry'),
    ('Truck', 'Truck'),
    ('Special Vehicle', 'Special Vehicle'),
    ('Cycle', 'Cycle'),
    ('Others', 'Others'),
    ]

class MerchantParkingAddVehicleTypeForm(forms.ModelForm):
    vehicle_type = forms.CharField(label="Vehicle Type",
        widget=forms.Select(choices=vehicle_type_choices,
            attrs={ 
                "placeholder" : "Vehicle Type",                
                "class": "form-control"
            }
        ),
    )

    class Meta:
        model = MerchantParkingAddVehicle
        fields = "__all__"
        exclude = ['user']

class MerchantParkingLotSpaceForm(forms.ModelForm):
    
    entry_gate = forms.BooleanField(required=True, label="Entry Gate",initial=True,
        widget=forms.CheckboxInput(
            attrs={ 
                "placeholder" : "Entry Gate",                
                "class": "form-control",
            }
        )
    )
    exit_gate = forms.BooleanField(required=False, label="Exit Gate",
        widget=forms.CheckboxInput(
            attrs={ 
                "placeholder" : "Exit Gate",                
                "class": "form-control",
            }
        )
    )
    vehicle_type = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Vehicle Type",                
                "class": "form-control"
            }
        )
    )
    spaces_count = forms.CharField(label="Space Count",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Space Count",                
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = MerchantParkingLotSpace
        fields = "__all__"
        exclude = ['user', 'vehicle_type_id']

class MerchantParkingLotSpaceChargesForm(forms.ModelForm):
    charges_by_choices = (
        ('One Time', 'One Time'),
        # ('Hourly', 'Hourly'),
    )
    vehicle_type = forms.CharField(
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Vehicle Type",                
                "class": "form-control"
            }
        )
    )
    charges_by = forms.CharField(widget=forms.HiddenInput(), initial="One Time")
    # charges_by = forms.CharField(label="Charges By",
    #     widget=forms.Select(
    #         attrs={ 
    #             "placeholder" : "Charges By",                
    #             "class": "form-control",
    #             "value": "One Time"
    #         }
    #     ),
    #     choices=charges_by_choices
    # )
    # charges_by = forms.ChoiceField(label="Charges By",
    #     widget=forms.Select(
    #         attrs={ 
    #             "placeholder" : "Charges By",                
    #             "class": "form-control",
    #             "value": "One Time"
    #         }
    #     ),
    #     choices=charges_by_choices
    # )
    charges = forms.CharField(label="Charges", 
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Charges",                
                "class": "form-control",
            }
        )
    )

    hour_choices = (
        ('1', '1 Hour'),
        ('2', '2 Hours'),
        ('3', '3 Hours'),
        ('4', '4 Hours'),
        ('5', '5 Hours'),
        ('6', '6 Hours'),
        ('7', '7 Hours'),
        ('8', '8 Hours'),
        ('9', '9 Hours'),
        ('10', '10 Hours'),
        ('11', '11 Hours'),
        ('12', '12 Hours'),
        ('13', '13 Hours'),
        ('14', '14 Hours'),
        ('15', '15 Hours'),
        ('16', '16 Hours'),
        ('17', '17 Hours'),
        ('18', '18 Hours'),
        ('19', '19 Hours'),
        ('20', '20 Hours'),
        ('21', '21 Hours'),
        ('22', '22 Hours'),
        ('23', '23 Hours'),
        ('24', '24 Hours'),
    )

    for_hours = forms.ChoiceField(label="Hours", 
        widget=forms.Select(
            attrs={ 
                "placeholder" : "Hours",                
                "class": "form-control",
            }
        ),
        choices=hour_choices
    )
    # for_hours = forms.CharField(label="Hours", 
    #     widget=forms.TextInput(
    #         attrs={ 
    #             "placeholder" : "Hours",                
    #             "class": "form-control",
    #         }
    #     )
    # )
    # for_additional_hours = forms.CharField(label="Hours", 
    #     widget=forms.TextInput(
    #         attrs={ 
    #             "placeholder" : "For Additional Hours",                
    #             "class": "form-control",
    #             "value": 0
    #         }
    #     )
    # )
    for_additional_hours = forms.ChoiceField(label="Hours", 
        widget=forms.Select(
            attrs={ 
                "placeholder" : "For Additional Hours",                
                "class": "form-control",
                
            }
        ),
        choices=hour_choices
    )

    additional_hours_charges = forms.CharField(label="Additional Hours Charges", required=False,
        widget=forms.NumberInput(
            attrs={ 
                "placeholder" : "Charges",                
                "class": "form-control",
                "value": 0
            }
        )
    )
    
    class Meta:
        model = MerchantParkingSpaceCharges
        fields = "__all__"
        exclude = ['user', 'vehicle_type_id']


class MerchantAddonPetrolPumpProductForm(forms.ModelForm):
    # product_id = forms.CharField(label="Product Id",
    #     widget=forms.TextInput(
    #         attrs={ 
    #             "placeholder" : "Product Id",                
    #             "class": "form-control",
    #         }
    #     )
    # )
    product_name = forms.CharField(label="Product Name",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Product Name",                
                "class": "form-control",
            }
        )
    )
    product_cost = forms.CharField(label="Product Cost",
        widget=forms.TextInput(
            attrs={ 
                "placeholder" : "Product Cost",                
                "class": "form-control"
            }
        )
    )
    product_availability = forms.ChoiceField(label="Product Availability",
        widget=forms.Select(
            attrs={ 
                "placeholder" : "Product Availability",                
                "class": "form-control"
            }
        ),
        choices=(
        ('', 'Select Product Availability'),
        ('Yes', 'Yes'),
        ('No', 'No')
        ),
    )
    class Meta:
        model = MerchantPetrolPump
        fields = "__all__"
        exclude = ['user']



class merchantuploadlogoForm(forms.Form):
    merchantlogofile = forms.FileField()
    mer_setting_id = forms.HiddenInput()


class merchantuploadstampForm(forms.Form):
    merchantstampfile = forms.FileField()


class merchantuploadsignatureForm(forms.Form):
    merchantsignaturefile = forms.FileField()



nozzel_choices= [
    ('','Select Nozzel'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ]

class AddPetrolNozzleForm(forms.ModelForm):
    nozzle = forms.CharField(label="Nozzle Number",
        widget=forms.Select(choices=nozzel_choices,
            attrs={ 
                "placeholder" : "Nozzle Number",                
                "class": "form-control",
            }
        )
    )
    class Meta:
        model = MerchantPetrolNozzle
        fields = "__all__"
        exclude = ['user']



class MerchantParkingLotPassChargesForm(forms.ModelForm):
    # vehicle_type = forms.CharField(label="Vehicle Type",
    #     widget=forms.Select(choices=vehicle_type_choices,
    #         attrs={ 
    #             "placeholder" : "Vehicle Type",                
    #             "class": "form-control"
    #         }
    #     ),
    # )
    per_visit_charges = forms.CharField(label="Per Visit Charges",required=False,
         widget=forms.NumberInput(
            attrs={ 
                "placeholder" : "Per Visit Charges",                
                "class": "form-control",
            }
        )
    )
    monthly_charges = forms.CharField(label="Monthly Charges",required=False,
         widget=forms.NumberInput(
            attrs={ 
                "placeholder" : "Monthly Charges",                
                "class": "form-control",
            }
        )
    )
    quarterly_charges = forms.CharField(label="Quarterly Charges",required=False,
         widget=forms.NumberInput(
            attrs={ 
                "placeholder" : "Quarterly Charges",                
                "class": "form-control",
            }
        )
    )
    half_yearly_charges = forms.CharField(label="Half Yearly Charges",required=False,
         widget=forms.NumberInput(
            attrs={ 
                "placeholder" : "Half Yearly Charges",                
                "class": "form-control",
            }
        )
    )
    yearly_charges = forms.CharField(label="Yearly Charges",required=False,
         widget=forms.NumberInput(
            attrs={ 
                "placeholder" : "Yearly Charges",                
                "class": "form-control",
            }
        )
    )
    class Meta:
        model = MerchantParkingLotPassCharges
        fields = "__all__"
        exclude = ['user', 'vehicle_type_id']


class PaymentSettingForm(forms.Form):
    payu_key = forms.CharField()
    payu_salt = forms.CharField()
    upi_id = forms.CharField()
    # choice = forms.CharField()