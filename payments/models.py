from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from users.models import GreenBillUser
from django.utils import timezone

class OwnerPaymentLinks(models.Model):
    mobile_no = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=True)
    amount = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    payment_done = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_url = models.CharField(max_length=1000, null=True)
    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True,)

    payment_mode = models.CharField(max_length=100, null=True)

    check_transaction_id = models.CharField(max_length=100, null=True)
    promotions = models.BooleanField(default=False)

class SendPaymentManually(models.Model):
    business_id = models.CharField(max_length=20, null=False)
    partner_id = models.CharField(max_length=20, null=False)
    bank_transaction_id = models.CharField(max_length=100, null=True)
    cheque_id = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True,)
    payment_mode = models.CharField(max_length=100, null=True)
    amount = models.CharField(max_length=100, null=True)
    payment_for = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)



