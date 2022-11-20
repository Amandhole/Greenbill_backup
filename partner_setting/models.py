from django.db import models
from users.models import GreenBillUser
from django.utils import timezone

class PartnerPaymentSetting(models.Model):
    partner_id = models.CharField(max_length=100)
    payu_key = models.CharField(max_length=100, null=False)
    payu_salt = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(default=timezone.now)



class PartnerSmsSetting(models.Model):
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    sms_header = models.CharField(max_length=10)
    status = models.BooleanField(default=0)