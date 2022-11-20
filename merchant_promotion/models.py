from django.db import models
from users.models import GreenBillUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone



class bulkMailSmsMerchantCustomerModel(models.Model):
    owner_id = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null=True)
    receiver = models.CharField(max_length=200, null=True)
    smsheader = models.CharField(max_length=50, null=True)
    template = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=200, null=True)
    message = RichTextUploadingField(null=True)
    o_sent_sms = models.BooleanField(null=True, default="0")
    o_sent_mail = models.BooleanField(null=True, default="0")
    created_at = models.DateTimeField(default=timezone.now)
    receiver_name = models.CharField(max_length=50, null=True)
    transactional = models.CharField(max_length=20, null=True)
    sent_status = models.CharField(max_length=120, null=True)

    customer_city = models.CharField(max_length = 150, null= True)
    customer_state = models.CharField(max_length = 150, null= True)
    customer_area = models.CharField(max_length = 150, null= True)
    sms_count = models.CharField(max_length = 150, null= True)
    campaign_name = models.CharField(max_length=500, default="Test Campaign")




class smsHeaderModel(models.Model):
    request_user = models.ForeignKey(GreenBillUser, on_delete = models.CASCADE)
    status = models.CharField(max_length=200, null=True)
    Active_status = models.BooleanField(null=True, default=False)
    header_content = models.CharField(max_length=12, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    header_type = models.CharField(max_length=50, default="Transactional")


class templateContentModel(models.Model):
    request_user = models.ForeignKey(GreenBillUser, on_delete = models.CASCADE)
    status = models.CharField(max_length=200, null=True)
    Active_status = models.BooleanField(null=True, default=False)
    template_content = models.CharField(max_length=200, null=True)
    sms_header = models.CharField(max_length=200, null=True) 
    created_at = models.DateTimeField(default=timezone.now)
    template_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.template_content