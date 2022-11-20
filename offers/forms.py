from django import forms
from .models import OfferModel



# class OffersForm(forms.ModelForm):
#     sms_chk = forms.BooleanField()
#     email_chk = forms.BooleanField(required=False)

# class OfferForm(forms.Form):
#     offer_name=forms.CharField(max_length = 150)
#     offer_caption=forms.CharField(max_length = 150)
#     offer_image=forms.ImageField()
#     valid_from=forms.DateField()
#     valid_through=forms.DateField()


class OfferForm(forms.Form):
    offer_name=forms.CharField(max_length = 150)
    offer_caption=forms.CharField(max_length = 150)
    valid_from=forms.DateField()
    valid_through=forms.DateField()
    offer_image=forms.ImageField()
    disapproved_reason=forms.CharField(max_length = 150)
    status=forms.CharField(max_length = 150)
    Offer_type = forms.CharField()
    offer_business_category = forms.CharField()
    offer_logo=forms.ImageField()
    business_name=forms.CharField(max_length = 150)
    offer_panel=forms.CharField(max_length = 150)




    


    