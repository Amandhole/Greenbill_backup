
from django import forms
from django.db import models
from django.db.models import fields
from .models import  bulkMailSmsModel
from ckeditor_uploader.fields import RichTextUploadingField

class MailSmsForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    
    message = forms.CharField(max_length=5000, required=False)



class bulkMailSmsForm(forms.ModelForm):
    class Meta:
        model = bulkMailSmsModel
        fields = ('message',)



