from django import forms
from .models import ReferralModel

class referralForm(forms.Form):
    recharge_amount_per_refferal = forms.CharField(required=True)
    recharge_amount_per_referent = forms.CharField(required=True)