from django import forms
from django.db import models
from django.db.models import fields
from .models import StampModel

class stampforms(forms.Form):
    content = models.CharField()
    colour = models.CharField()
    stampdesgn = models.CharField()

class stampuploadForms(forms.Form):
    m_business_stamp = forms.ImageField(required=False)






