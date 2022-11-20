from django.db import models
from subscription_plan.models import subscription_plan_details
from users.models import GreenBillUser
from django.utils import timezone

class partner_subscriptions(models.Model):
    subscription_id = models.CharField(blank=True, null=True, max_length = 500)
    subscription_name = models.CharField(blank=True, null=True, max_length = 500)
    partner_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE)

    valid_for_month = models.CharField(blank=True, null=True, max_length=100)
    per_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_url_cost = models.CharField(blank=True, null=True, max_length=100)

    recharge_amount = models.FloatField(blank=True, null=True)
    total_amount_avilable = models.FloatField(blank=True, null=True)

    purchase_cost = models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(default=timezone.now)
    expiry_date = models.CharField(blank=True, null=True, max_length=100)

    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)
    # b_transaction_id = models.CharField(max_length=100, null=True)
    # check_no = models.CharField(max_length=100, null=True)

    is_active = models.BooleanField(default=False, null=True)

class partner_promotional_sms_subscriptions(models.Model):
    subscription_id = models.CharField(blank=True, null=True, max_length = 500)
    subscription_name = models.CharField(blank=True, null=True, max_length = 500)
    partner_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE)

    total_sms = models.CharField(blank=True, null=True, max_length = 100)
    per_sms_cost = models.CharField(blank=True, null=True, max_length = 100)

    total_sms_avilable = models.FloatField(blank=True, null=True)

    purchase_cost = models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(default=timezone.now)

    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)

    is_active = models.BooleanField(default=False, null=True)

class partner_transactional_sms_subscriptions(models.Model):
    subscription_id = models.CharField(blank=True, null=True, max_length = 500)
    subscription_name = models.CharField(blank=True, null=True, max_length = 500)
    partner_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE)

    total_sms = models.CharField(blank=True, null=True, max_length = 100)
    per_sms_cost = models.CharField(blank=True, null=True, max_length = 100)

    total_sms_avilable = models.FloatField(blank=True, null=True)

    purchase_cost = models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, null=True)

    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)

class partner_recharge_history(models.Model):
    subscription_plan_id = models.CharField(blank=True, null=True, max_length = 500)
    subscription_name = models.CharField(blank=True, null=True, max_length = 500)
    partner_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.SET_NULL)

    valid_for_month = models.CharField(blank=True, null=True, max_length=100)
    per_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_url_cost = models.CharField(blank=True, null=True, max_length=100)

    total_sms = models.CharField(blank=True, null=True, max_length = 100)
    per_sms_cost = models.CharField(blank=True, null=True, max_length = 100)

    is_subscription_plan = models.BooleanField(default=False, null=True)
    is_promotional_sms_plan = models.BooleanField(default=False, null=True)
    is_transactional_sms_plan = models.BooleanField(default=False, null=True)
    is_add_on_plan = models.BooleanField(default=False, null=True)

    cost = models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(default=timezone.now)
    expiry_date = models.CharField(blank=True, null=True, max_length=100)

    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)

    invoice_no = models.CharField(max_length=120, null=True, default='GB')
    mode = models.CharField(max_length=100, null=True)
    bank_transaction_id = models.CharField(max_length=100, null=True)
    cheque_no = models.CharField(max_length=100, null=True)
    gst_amount = models.CharField(max_length=100, null=True)

class partner_subscriptions_keys(models.Model):
    key = models.CharField(blank=True, null=True, max_length = 1000)
    created_at = models.DateTimeField(default=timezone.now)
