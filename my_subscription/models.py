from django.db import models
from subscription_plan.models import subscription_plan_details
from users.models import GreenBillUser
from django.utils import timezone

class merchant_subscriptions(models.Model):
    subscription_id = models.CharField(blank=True, null=True, max_length = 500)
    subscription_name = models.CharField(blank=True, null=True, max_length = 500)
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE)
    business_ids = models.CharField(blank=True, null=True, max_length = 1000)

    valid_for_month = models.CharField(blank=True, null=True, max_length=100)
    per_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)

    recharge_amount = models.FloatField(blank=True, null=True)
    total_amount_avilable = models.FloatField(blank=True, null=True)

    purchase_cost = models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(default=timezone.now)
    expiry_date = models.CharField(blank=True, null=True, max_length=100)

    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)

    is_active = models.BooleanField(default=False, null=True)


    one_month_expiry = models.BooleanField(default=False, null=True)
    one_week_expiry = models.BooleanField(default=False, null=True)
    expired_plan = models.BooleanField(default=False, null=True)

    no_of_users = models.CharField(max_length=100, null=True)
    gst_amount = models.CharField(max_length=100, null=True)
    merchant_business_id = models.CharField(max_length=100, null=True)
    

class promotional_sms_subscriptions(models.Model):
    subscription_id = models.CharField(blank=True, null=True, max_length = 500)
    subscription_name = models.CharField(blank=True, null=True, max_length = 500)
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE)
    business_ids = models.CharField(blank=True, null=True, max_length = 1000)

    total_sms = models.CharField(blank=True, null=True, max_length = 100)
    per_sms_cost = models.CharField(blank=True, null=True, max_length = 100)

    total_sms_avilable = models.FloatField(blank=True, null=True)

    purchase_cost = models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, null=True)

    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)

   
    low_sms_balance = models.BooleanField(default=False, null=True)

    


class transactional_sms_subscriptions(models.Model):
    subscription_id = models.CharField(blank=True, null=True, max_length = 500)
    subscription_name = models.CharField(blank=True, null=True, max_length = 500)
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE)
    business_ids = models.CharField(blank=True, null=True, max_length = 1000)

    total_sms = models.CharField(blank=True, null=True, max_length = 100)
    per_sms_cost = models.CharField(blank=True, null=True, max_length = 100)

    total_sms_avilable = models.FloatField(blank=True, null=True)

    purchase_cost = models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, null=True)

    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)

    
    low_sms_balance = models.BooleanField(default=False, null=True)


    
class recharge_history(models.Model):
    subscription_plan_id = models.CharField(blank=True, null=True, max_length = 500)
    subscription_name = models.CharField(blank=True, null=True, max_length = 500)
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.SET_NULL)
    business_ids = models.CharField(blank=True, null=True, max_length = 500)
    
    valid_for_month = models.CharField(blank=True, null=True, max_length=100)
    per_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)

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

    invoice_no = models.CharField(max_length=120, null=True)
    mode = models.CharField(max_length=100, null=True)
    cheque_no = models.CharField(max_length=100, null=True)

    bank_transaction_id = models.CharField(max_length=120,null=True)

    no_of_users = models.CharField(max_length=100, null=True)
    gst_amount = models.CharField(max_length=100, null=True)
    merchant_business_id = models.CharField(max_length=100, null=True)

class merchant_subscriptions_keys(models.Model):
    key = models.CharField(blank=True, null=True, max_length = 1000)
    created_at = models.DateTimeField(default=timezone.now)

class sent_bill_history(models.Model):
    subscription_id = models.CharField(max_length=100, blank=True)
    user_id = models.CharField(max_length=100, blank=True)
    mobile_no = models.CharField(max_length=100, blank=True, default='')
    m_business_id = models.CharField(max_length=200, blank=True, default='')

    green_bill_transaction = models.BooleanField(default=False)
    green_bill_print_transaction = models.BooleanField(default=False)
    print_transaction = models.BooleanField(default=False)
    
    digital_bill = models.BooleanField(default=False)
    sms_bill = models.BooleanField(default=False)

    bill_amount = models.CharField(max_length=100, blank=True)
    bill_cost = models.CharField(max_length=100, blank=True)

    merchant_bill = models.BooleanField(default=False)
    customer_bill = models.BooleanField(default=False)
    parking_bill = models.BooleanField(default=False)
    petrol_bill = models.BooleanField(default=False)

    created_at =  models.DateTimeField(default=timezone.now)

    is_exe = models.BooleanField(default=False)

class contact_for_subscriptions_requirements(models.Model):
    contact_no = models.CharField(max_length=20, null=True)
    contact_email_id = models.EmailField(blank=True, null=True)
    contact_name = models.CharField(blank=True, null=True, max_length = 100)
    contact_requirements = models.CharField(blank=True, null=True, max_length = 1000)
    date_and_time = models.DateTimeField(default=timezone.now)
    subscription_name = models.CharField(blank=True, null=True, max_length = 100)