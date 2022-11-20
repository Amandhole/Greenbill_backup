from django.db import models
from django.utils import timezone

class subscription_plan_details(models.Model):
    subscription_name = models.CharField(blank=True, null=True, max_length=500)
    valid_for_month = models.CharField(blank=True, null=True, max_length=100)
    per_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_url_cost = models.CharField(blank=True, null=True, max_length=100)
    software_maintainace_cost = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount = models.CharField(blank=True, null=True, max_length=100)

    discount_in = models.CharField(blank=True, null=True, max_length=100)
    discount_percentage = models.CharField(blank=True, null=True, max_length=100)
    discount_amount = models.CharField(blank=True, null=True, max_length=100)

    user_type = models.CharField(blank=True, null=True, max_length=100)
    subscription_plan_cost = models.CharField(blank=True, null=True, max_length=100)

    business_category = models.CharField(max_length=20000, blank=True, null=True, default='')
    merchant_name = models.CharField(max_length=20000, blank=True, null=True, default='')
    customized_plan_for = models.CharField(blank=True, null=True, max_length=100)
    customized_plan = models.BooleanField(default=False, null=True)

    suited_for = models.CharField(blank=True, null=True, max_length=1000)

    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, null=True)
    is_offer = models.BooleanField(default=False, null=True)

    number_of_users = models.CharField(blank=True, null=True, max_length=100, default="0")

    cost_for_users = models.CharField(blank=True, null=True, max_length=100, default="0")

    gst_amount = models.CharField(blank=True, null=True, max_length=100, default="0")

    merchant_number_of_users = models.CharField(blank=True, null=True, max_length=100, default="0")

    merchant_gst = models.CharField(blank=True, null=True, max_length=100, default="0")

    loyalty_point = models.CharField(blank=True, null=True, max_length=100)


class promotional_subscription_plan_model(models.Model):
    subscription_name = models.CharField(blank=True, null=True, max_length=500)
    total_sms = models.CharField(max_length=200, null=True, default="")
    per_sms_cost = models.CharField(max_length=200, null=True, default="")
    total_sms_cost = models.CharField(max_length=200, null=True, default="")
    
    discount_in = models.CharField(blank=True, null=True, max_length=100)
    discount_percentage = models.CharField(blank=True, null=True, max_length=100)
    discount_amount = models.CharField(blank=True, null=True, max_length=100)
    
    user_type = models.CharField(blank=True, null=True, max_length=100,default="all")
   
    business_category = models.CharField(max_length=20000, blank=True, null=True, default='')
    merchant_name = models.CharField(max_length=20000, blank=True, null=True, default='')
    customized_plan_for = models.CharField(blank=True, null=True, max_length=100, default='')
    customized_plan = models.BooleanField(default=False, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, null=True)
    total_sms_avilable = models.CharField(max_length=200, null=True , default="")
    gst_amount = models.CharField(blank=True, null=True, max_length=100, default="0")

    actual_total_amount = models.CharField(blank=True, null=True, max_length = 100)

class transactional_subscription_plan_model(models.Model):
    subscription_name = models.CharField(blank=True, null=True, max_length=500)
    total_sms = models.CharField(max_length=200, null=True, default="")
    per_sms_cost = models.CharField(max_length=200, null=True, default="")
    total_sms_cost = models.CharField(max_length=200, null=True, default="")
    
    discount_in = models.CharField(blank=True, null=True, max_length=100)
    discount_percentage = models.CharField(blank=True, null=True, max_length=100)
    discount_amount = models.CharField(blank=True, null=True, max_length=100)
    
    user_type = models.CharField(blank=True, null=True, max_length=100,default="all")
   
    business_category = models.CharField(max_length=20000, blank=True, null=True, default='')
    merchant_name = models.CharField(max_length=20000, blank=True, null=True, default='')
    customized_plan_for = models.CharField(blank=True, null=True, max_length=100, default='')
    customized_plan = models.BooleanField(default=False, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, null=True)
    total_sms_avilable = models.CharField(max_length=200, null=True , default="")
    gst_amount = models.CharField(blank=True, null=True, max_length=100, default="0")

    actual_total_amount = models.CharField(blank=True, null=True, max_length = 100)

class add_on_plan_model(models.Model):
    add_on_name = models.CharField(blank=True, null=True, max_length=500)
    
    per_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_bill_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_receipt_cost = models.CharField(blank=True, null=True, max_length=100)
    per_digital_cash_memo_cost = models.CharField(blank=True, null=True, max_length=100)

    recharge_amount = models.CharField(blank=True, null=True, max_length=100)
    
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, null=True)
    gst_amount = models.CharField(blank=True, null=True, max_length=100, default="0")

    actual_total_amount = models.CharField(blank=True, null=True, max_length = 100)

    actual_final_amount = models.CharField(blank=True, null=True, max_length = 100)

    recharge_amount_one = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_two = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_three = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_four = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_five = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_six = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_seven = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_eight = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_nine = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_ten = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_eleven = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_twelve = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_thirteen = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_fourteen = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_fifteen = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_sixteen = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_seventeen = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_eighteen = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_nineteen = models.CharField(blank=True, null=True, max_length=100)
    recharge_amount_twenty = models.CharField(blank=True, null=True, max_length=100)


