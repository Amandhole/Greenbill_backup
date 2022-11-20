from django.db import models
from users.models import GreenBillUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone



class bulkMailSmsMerchantModel(models.Model):
    owner_id = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null=True)
    receiver = models.CharField(max_length=200, null=True)
    smsheader = models.CharField(max_length=50, null=True)
    template = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=200, null=True)
    message = RichTextUploadingField(null=True)
    o_sent_sms = models.BooleanField(null=True, default="0")
    o_sent_mail = models.BooleanField(null=True, default="0")
    created_at = models.DateTimeField(default=timezone.now)
    receiver_name= models.CharField(max_length=120, null=True)


class MerchantDisablereasons(models.Model):
    merchant_reason = models.CharField(max_length=50, null=True, default="")
    created_date =  models.DateTimeField(default=timezone.now)