from django import forms
from django.db import models
from django.db.models import fields
from .models import availmodels


class availforms(forms.Form):
    lover_price = models.CharField()