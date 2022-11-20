from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from .models import *

class SystemUpdateForm(forms.ModelForm):
    class Meta:
        model = system_updates
        fields = ('message',)