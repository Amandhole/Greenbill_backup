from django import forms
from .models import MerchantEnquiryModel


class MerchantEnquiryForm(forms.ModelForm):
    """
    Digital Marketing Merchant Enquiry Form
    """
    comments = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MerchantEnquiryModel
        exclude = ['enquary_status', 'mer_id']
