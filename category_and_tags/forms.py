from django import forms

class BusinessCategoryForm(forms.Form):
    business_category_name = forms.CharField(required=True)
    business_category_description = forms.CharField(required=False)

class BusinessCategoryEditForm(forms.Form):
    edit_business_category_name = forms.CharField(required=True)
    edit_business_category_description = forms.CharField(required=False)

class BillCategoryForm(forms.Form):
    bill_category_name = forms.CharField(required=True)
    bill_category_description = forms.CharField(required=False)
    bill_category_icon = forms.ImageField(required=True)

class BillCategoryEditForm(forms.Form):
    edit_bill_category_name = forms.CharField(required=True)
    edit_bill_category_description = forms.CharField(required=False)
    edit_bill_category_icon = forms.ImageField(required=False)

class BillTagsForm(forms.Form):
    bill_tags_name = forms.CharField(required=True)
    bill_tags_description = forms.CharField(required=False)

class BillTagsEditForm(forms.Form):
    edit_bill_tags_name = forms.CharField(required=True)
    edit_bill_tags_description = forms.CharField(required=False)