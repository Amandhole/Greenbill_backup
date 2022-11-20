from django import forms
from .models import Customer_Info_Model


class Customer_Info_Form(forms.Form):
    cust_first_name = forms.CharField(required=True)
    cust_last_lname = forms.CharField(required=True)
    cust_email = forms.EmailField(required=False)
    cust_mobile_num = forms.CharField(required=True)
    customer_state = forms.CharField(required=False)
    customer_city = forms.CharField(required=False)
    customer_area = forms.CharField(required=False)
    customer_pin_code = forms.IntegerField(required=False)


class Edit_Customer_Info_Form(forms.Form):
    edit_fname = forms.CharField(max_length=50)
    edit_lname = forms.CharField(max_length=50)
    edit_email = forms.EmailField()
    edit_mobile = forms.CharField(max_length=20)
    edit_area = forms.CharField(max_length=20)
    edit_pin_code = forms.CharField(max_length=20)
