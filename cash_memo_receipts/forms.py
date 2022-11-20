from django import forms


class Cash_Memo_Form(forms.Form):
    users_id = forms.CharField(required=False)
    memo_name = forms.CharField(required=False)
    header_text = forms.CharField(required=False)
    footer_text = forms.CharField(required=False)
    stamp_image = forms.ImageField(required=False)
    favcolor = forms.CharField(required=False)


class ReceiptsForm(forms.Form):
    receipts_name = forms.CharField(required=False)
    header_text = forms.CharField(required=False)
    footer_text = forms.CharField(required=False)
    stamp_image = forms.ImageField(required=False)
    favcolor = forms.CharField(required=False)
