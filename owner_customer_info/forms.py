from django import forms
from customer_info.models import Customer_Info_Model
from .models import *

class CustomerForm(forms.Form):
    cust_first_name=forms.CharField()
    cust_last_lname=forms.CharField()
    cust_email=forms.EmailField()
    cust_mobile_num=forms.CharField()
    customer_area=forms.CharField()
    customer_pin_code=forms.IntegerField()



class bulkMailSmsCustomerForm(forms.ModelForm):
    class Meta:
        model = bulkMailSmsCustomerModel
        fields = ('message',)