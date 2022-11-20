from datetime import date
from os import name, truncate
from django.db import models
from datetime import datetime
from users.models import GreenBillUser, MerchantProfile, Merchant_users

# Create your models here.


class Cash_Memo_Design_Model(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    memo_design_image = models.ImageField(
        upload_to="Cash_Memo_Design/", null=True, default="")
    paper_size = models.CharField(max_length=500, null=True, default="")
    read_status = models.BooleanField(default=False, null=True)
    comments = models.CharField(max_length=1000, default="", null=True,)
    created_at = models.DateTimeField(default=datetime.now)
    notes = models.CharField(max_length=1000, default="", null=True,)
    status = models.CharField(max_length=100,null=True)


class CustomerCashMemoDetailModels(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    memo_no = models.CharField(max_length=120, null=True, default='')
    name = models.CharField(max_length=120, null=True, default='')
    address = models.CharField(max_length=120, null=True, default='')
    mobile_number = models.CharField(max_length=10, null=True,default='')
    date = models.DateField(null=True, default='')
    memo_url = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=120, null=True, default='',)
    quantity = models.CharField(max_length=120, null=True, default='', )
    rate = models.CharField(max_length=120, null=True, default='', )
    amount = models.CharField(max_length=120, null=True, default='', )
    term_and_condition1 = models.CharField(max_length=120, null=True)
    term_and_condition2 = models.CharField(max_length=120, null=True)
    term_and_condition3 = models.CharField(max_length=120, null=True)
    authorised_sign = models.FileField(null=True, blank=True, upload_to='memo_authorised_sign', default="")

    template_choice = models.CharField(max_length=20, null=True, default='')
    total = models.CharField(max_length=50, null=True, default='')
    total_in_words = models.CharField(max_length=120, null=True,default='')
    stamp_last_record = models.CharField(max_length=120, null=True,default='')
    is_stamp_type = models.CharField(max_length=120, null=True,default='')
    rejected_cash_memo = models.BooleanField(blank=True, default=False)
    rejected_reason = models.CharField(max_length=120, null=True,default='')


class CustomerReceiptDetailsModels(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    receipt_no = models.CharField(max_length=120, null=True, default='')
    mobile_number = models.CharField(max_length=10, null=True)
    receipt_url = models.CharField(max_length=200, null=True,default='')
    cash_received_from = models.CharField(max_length=120, null=True, default='')
    rs = models.CharField(max_length=120, null=True,default='')
    # advnaced = models.CharField(max_length=120, null=True,default='')
    amount_for = models.CharField(max_length=120,null=True, default='')
    date = models.DateField(null=True, default='')
    # receipt_url = models.CharField(max_length=120, null=True, default='')
    template_choice = models.CharField(max_length=20, null=True, default='')
    total = models.CharField(max_length=50, null=True, default='')
    # total_in_words = models.CharField(max_length=120, null=True,default='')
    grand_total = models.CharField(max_length=120,null=True,default='')
    term_and_condition1 = models.CharField(max_length=120, null=True)
    term_and_condition2 = models.CharField(max_length=120, null=True)
    term_and_condition3 = models.CharField(max_length=120, null=True)
    authorised_sign = models.FileField(null=True, blank=True, upload_to='receipt_authorised_sign', default="")
    received_in_cash = models.CharField(max_length=50,null=True,default='')
    received_in_cheque = models.CharField(max_length=50,null=True,default='')
    received_in_other = models.CharField(max_length=50,null=True,default='')
    stamp_last_record = models.CharField(max_length=120, null=True,default='')
    is_stamp_type = models.CharField(max_length=120, null=True,default='')
    rejected_receipt = models.BooleanField(blank=True, default=False)
    rejected_reason = models.CharField(max_length=120, null=True,default='')

class save_template_for_cashmemo(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    template = models.CharField(max_length = 150, null= True)

class save_template_for_receipt(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    template = models.CharField(max_length = 150, null= True)    
    
class save_stamp_for_cashmemo(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    stamp_id_cashmemo = models.CharField(max_length = 150, null= True)

class save_stamp_for_receipt(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    stamp_id_cashmemo = models.CharField(max_length = 150, null= True)


class cash_memo_template_images(models.Model):
    template_id = models.CharField(null=True, blank=True, max_length=20)
    img_url = models.ImageField(null=True, blank=True, upload_to='cash_receipt_images/', default="")