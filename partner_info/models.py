from django.db import models

from users.models import GreenBillUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# Create your models here.

class bulkMailSmsPartnerModel(models.Model):
    owner_id = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null=True)
    receiver = models.CharField(max_length=200, null=True)
    smsheader = models.CharField(max_length=50, null=True)
    template = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=200, null=True)
    message = RichTextUploadingField(null=True)
    o_sent_sms = models.BooleanField(null=True, default="0")
    o_sent_mail = models.BooleanField(null=True, default="0")
    created_at = models.DateTimeField(default=timezone.now)
    transactional = models.CharField(max_length=20, null=True)
    sent_status = models.CharField(max_length=120,null=True)

    customer_city = models.CharField(max_length = 150, null= True)
    customer_state = models.CharField(max_length = 150, null= True)
    customer_area = models.CharField(max_length = 150, null= True)
    sms_count = models.CharField(max_length = 150, null= True)

    merchant_city = models.CharField(max_length = 150, null= True)
    merchant_state = models.CharField(max_length = 150, null= True)
    merchant_area = models.CharField(max_length = 150, null= True)



class PartnerdiasbleReasons(models.Model):
    partner_reason = models.CharField(max_length=50, null=True, default="")
    created_date =  models.DateTimeField(default=timezone.now)

class PartnerMonthlyCommision(models.Model):
    p_mobile_no = models.CharField(max_length=500, null=True, blank=True)
    month = models.CharField(max_length=500, null=True, blank=True)
    amount = models.CharField(max_length=500, null=True, blank=True)
    year = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=500, null=True, blank=True)

class csvfileupload(models.Model):
    csv_file = models.FileField(null=True,blank=True, upload_to='merchant_address_proof', default="")

class SampleExcelFile(models.Model):
    sample_excel_file = models.FileField(null=True,blank=True, upload_to='merchant_address_proof', default="")
        
