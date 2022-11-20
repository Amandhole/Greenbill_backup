from django import forms

class RoleForm(forms.Form):
    role_name = forms.CharField()
    role_description = forms.CharField(required=False)

class RoleForm_edit(forms.Form):
    edit_role_name = forms.CharField()
    edit_role_description = forms.CharField(required=False)

class RoleAssign_form(forms.Form):
    auth_id = forms.CharField(required=False)
    role_name = forms.CharField(required=True)
    user_role_id = forms.IntegerField(required=False)