from django import forms
from django.db import models
from django.db.models import fields
from .models import statusmodels


class statusforms(forms.Form):
    name = models.CharField()
    caption = models.CharField()