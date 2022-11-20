from . models import OwnerCouponModel
from django import forms


class OwnerCouponsForm(forms.Form):
    coupon_name = forms.CharField(required=False)
    valid_from = forms.CharField(required=False)
    valid_through = forms.CharField(required=False)
    coupon_code = forms.CharField(required=False)
    coupon_value = forms.CharField(required=False)
    green_point = forms.CharField(required=False)
    coupon_logo = forms.ImageField(required=False)

