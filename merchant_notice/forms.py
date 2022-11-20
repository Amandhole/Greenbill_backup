from django import forms
from .models import Merchant_Notice_Model


class Notice_Form(forms.Form):
    notice_title = forms.CharField(max_length=100, required=False)
    notice_file = forms.FileField(required=False)
    message = forms.CharField(max_length=5000, required=False)
