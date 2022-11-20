from django import forms
from .models import ShareOfferModel

class OfferImageForm(forms.Form):
    share_offer_image=forms.ImageField()


