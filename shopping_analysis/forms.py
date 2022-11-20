from django import forms

class ShoppingAnalysisForm(forms.Form):
    from_date = forms.DateField(required=True)
    to_date = forms.DateField(required=True)