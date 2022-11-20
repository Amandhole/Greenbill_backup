from django import forms

class Customer_Bill_Form(forms.Form):
    cust_bill = forms.FileField()
    bill_amount = forms.FloatField()
    bill_date = forms.DateField()