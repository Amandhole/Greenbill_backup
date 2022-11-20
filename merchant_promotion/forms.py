from django import forms
from .models import bulkMailSmsMerchantCustomerModel


class bulkMailSmsMerchantCustomerForm(forms.ModelForm):
    class Meta:
        model = bulkMailSmsMerchantCustomerModel
        fields = ('message',)
