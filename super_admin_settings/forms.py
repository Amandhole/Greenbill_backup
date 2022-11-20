from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from .models import *

class EmailTemplatesForm(forms.ModelForm):
    class Meta:
        model = email_templates
        fields = "__all__"

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = notification_settings
        fields = ('message',)

class smsSettingForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    sender_id = forms.CharField(required=True)
    status = forms.CharField(required=True)

class PaymentSettingForm(forms.Form):
    payu_key = forms.CharField(required=True)
    payu_salt = forms.CharField(required=True)

class GreenPointsForm(forms.Form):
    bill_points = forms.CharField(max_length = 150)
    referral_points = forms.CharField(max_length = 150)  