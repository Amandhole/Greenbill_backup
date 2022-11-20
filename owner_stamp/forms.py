from django import forms
from django.db import models
from django.db.models import fields
from .models import wstampmodels, stampdmodels

class wstampforms(forms.Form):
    stamp_name = forms.CharField()
    stamp_content = forms.CharField()
    option_color = forms.CharField()
    selection_design = forms.CharField() 
    
class stampdforms(forms.Form):
    name = forms.CharField() 

   




    