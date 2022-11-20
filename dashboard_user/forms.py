"""
Copyright (c) 2020 - present Hind Softwares
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings
User = settings.AUTH_USER_MODEL

class CreateUserForm(forms.Form): 
    mobile_no = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    role_name = forms.CharField()

class UpdateUserForm(forms.Form): 
    edit_mobile_no = forms.CharField()
    edit_email = forms.EmailField()
    edit_first_name = forms.CharField()
    edit_last_name = forms.CharField()
    edit_role_name = forms.CharField()
    user_id = forms.CharField()
