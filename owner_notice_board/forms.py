from django import forms


class ownerNoticeBoardForm(forms.Form):
    notice_title = forms.CharField(max_length=100, required=False)
    notice_file = forms.FileField(required=False)
    message = forms.CharField(max_length=5000, required=False)
