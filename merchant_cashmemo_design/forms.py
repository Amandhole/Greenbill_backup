
from django.db import models
from django.db.models import fields
from category_and_tags.models import business_category
from django import forms

class CustomerCashMemodetailsForm(forms.Form):
    memo_no = forms.CharField(required=False)
    name = forms.CharField(required=False)
    address = forms.CharField(required=False)
    mobile_number = forms.CharField(required=False)
    date = forms.DateField(required=False)
    total = forms.CharField(required=False)
    description = forms.CharField(required=False)
    quantity = forms.CharField(required=False)
    rate = forms.CharField(required=False)
    amount = forms.CharField(required=False)
    authorised_sign = forms.FileField(required=False)
    template_choice = forms.CharField(required=False)
    total_in_words = forms.CharField(required=False)    

class CustomerReceiptdetailsForm(forms.Form):
    receipt_no = forms.CharField(required=False)
    cash_received_from = forms.CharField(required=False)
    rs = forms.CharField(required=False)
    mobile_number = forms.CharField(required=False)
    amount_for = forms.CharField(required=False)
    # advnaced = forms.CharField(required=False)
    date = forms.DateField(required=False)
    template_choice = forms.CharField(required=False)
    total = forms.CharField(required=True)
    authorised_sign = forms.FileField(required=False)
    # total_in_words = forms.CharField(required=False)  
    grand_total = forms.CharField(required=False)
