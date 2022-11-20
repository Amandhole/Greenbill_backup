from django.db import models
from users.models import GreenBillUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
# Create your models here.


class availmodels(models.Model):
    lover_price = models.CharField(max_length=120, null=True)



class bulkMailSmsCustomerModel(models.Model):
    owner_id = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null=True)
    receiver = models.CharField(max_length=200, null=True)
    smsheader = models.CharField(max_length=50, null=True)
    template = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=200, null=True)
    message = RichTextUploadingField(null=True)
    o_sent_sms = models.BooleanField(null=True, default="0")
    o_sent_mail = models.BooleanField(null=True, default="0")
    created_at = models.DateTimeField(default=timezone.now)