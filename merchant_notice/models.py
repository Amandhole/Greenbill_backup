from django.db import models
from users.models import GreenBillUser
from django.utils import timezone
# Create your models here.


class Merchant_Notice_Model(models.Model):
    owner_id = models.ForeignKey(
        GreenBillUser, on_delete=models.CASCADE, null=True,)
    notice_title = models.CharField(max_length=100)
    notice_file = models.FileField(upload_to="NoticeDoc/")
    message = models.CharField(max_length=5000)
    m_sent_sms = models.BooleanField(null=True, default="0")
    m_sent_mail = models.BooleanField(null=True, default="0")
    m_notification = models.BooleanField(null=True, default="0")
    created_at = models.DateTimeField(default=timezone.now)
    receiver_name = models.CharField(max_length=20,null=True)



class merchant_notice_sent(models.Model):
    notice_id = models.ForeignKey(Merchant_Notice_Model, on_delete=models.CASCADE)
    user_id = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE)
    read_status = models.CharField(max_length=5, null=True, default="0")
    sent_sms = models.BooleanField(null=True, default="0")
    sent_mail = models.BooleanField(null=True, default="0")
    notification = models.BooleanField(null=True, default="0")
    sent_date = models.DateTimeField(default=timezone.now)
