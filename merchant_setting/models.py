from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

from users.models import GreenBillUser, MerchantProfile
from django.utils import timezone
from datetime import datetime


class MerchantEmailSetting(models.Model):
    from_name = models.CharField(max_length=100, null=False)
    from_email = models.CharField(max_length=100, null=False)
    footer = models.CharField(max_length=100, null=True)
    signature = models.CharField(max_length=100, null=True)

class MerchantSmsSetting(models.Model):
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    sms_header = models.CharField(max_length=10)
    status = models.BooleanField(default=0)


class Deleted_Bills_By_Days_setting(models.Model):
    m_user = models.ForeignKey(GreenBillUser, to_field="id" , null=True, on_delete=models.CASCADE)
    delete_days_merchant = models.CharField(default = '0',max_length=100)
    delete_days_customer = models.CharField(default = '0', max_length=100)
    delete_from_merchant = models.BooleanField(default=False)
    delete_from_customer = models.BooleanField(default=False)
    date_entered = models.DateTimeField(default=datetime.now)

class MerchantPetrolPump(models.Model):
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    m_business_id = models.CharField(max_length=100)
    product_id = models.CharField(max_length=200, default='', blank= True, null = True)
    product_name = models.CharField(max_length=100)
    product_cost = models.CharField(max_length=100, blank=False, null=False)
    product_availability = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MerchantParkingAddVehicle(models.Model):
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    m_business_id = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class MerchantParkingLotSpace(models.Model):
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    m_business_id = models.CharField(max_length=100)
    entry_gate = models.BooleanField(max_length=1, blank=True, null=True)
    exit_gate = models.BooleanField(max_length=1, null=True, blank=True)
    vehicle_type_id = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type = models.CharField(max_length=100, blank=True, null=True)
    spaces_count = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class MerchantParkingSpaceCharges(models.Model):
    charges_by_choices = (
        ('One Time', 'One Time'),
        # ('Hourly', 'Hourly'),
    )
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    m_business_id = models.CharField(max_length=100)
    vehicle_type_id = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100, blank=True, null=True)
    charges_by = models.CharField(max_length=100, choices=charges_by_choices)
    charges = models.CharField(max_length=100, null=False, blank=False)
    additional_hours_charges = models.CharField(max_length=100, null=True, default="")
    for_hours = models.CharField(max_length=100, null=True, blank=True)
    for_additional_hours = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class parking_app_setting_model(models.Model):
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE,)
    merchant_bussiness = models.ForeignKey(MerchantProfile, null=True, on_delete=models.CASCADE,)
    digital_bill = models.BooleanField(default=False)
    sms = models.BooleanField(default=False)
    entry_gate = models.BooleanField(default=True)
    exit_gate = models.BooleanField(default=False)
    footer_text1 = models.CharField(max_length=100, blank=True, null=True, default='')
    footer_text2 = models.CharField(max_length=100, blank=True, null=True, default='')
    footer_text3 = models.CharField(max_length=100, blank=True, null=True, default='')
    header_text1 = models.CharField(max_length=100, blank=True, null=True, default='')
    header_text2 = models.CharField(max_length=100, blank=True, null=True, default='')
    header_text3 = models.CharField(max_length=100, blank=True, null=True, default='')
    pay_bill_at_exit_gate = models.BooleanField(default=False)
    manage_space = models.BooleanField(default=False) 
    created_at = models.DateTimeField(default=timezone.now)

class petrol_pump_app_setting_model(models.Model):
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE,)
    merchant_bussiness = models.ForeignKey(MerchantProfile, null=True, on_delete=models.CASCADE,)
    digital_bill = models.BooleanField(default=False)
    sms = models.BooleanField(default=False)
    footer_text1 = models.CharField(max_length=1000, blank=True, null=True, default='')
    footer_text2 = models.CharField(max_length=1000, blank=True, null=True, default='')
    footer_text3 = models.CharField(max_length=1000, blank=True, null=True, default='')
    header_text1 = models.CharField(max_length=1000, blank=True, null=True, default='')
    header_text2 = models.CharField(max_length=1000, blank=True, null=True, default='')
    header_text3 = models.CharField(max_length=1000, blank=True, null=True, default='')
    created_at = models.DateTimeField(default=timezone.now)


class AddonPetrolPump(models.Model):
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    m_business_id = models.CharField(max_length=100)
    product_id = models.CharField(max_length=200)
    product_name = models.CharField(max_length=100)
    product_cost = models.CharField(max_length=100, blank=False, null=False)
    product_availability = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MerchantPetrolNozzle(models.Model):
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    m_business_id = models.CharField(max_length=100)
    nozzle = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class MerchantParkingLotPassCharges(models.Model):
    user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, blank=True, null=True)
    m_business_id = models.CharField(max_length=100)
    vehicle_type_id = models.CharField(max_length=100, null=True)
    pass_type = models.CharField(max_length=500, null=True)
    vehicle_type = models.CharField(max_length=500, blank=True, null=True)
    charges = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # per_visit_charges = models.CharField(max_length=500,null=True, default="")
    # monthly_charges = models.CharField(max_length=500,null=True, default="")
    # quarterly_charges = models.CharField(max_length=500,null=True, default="")
    # half_yearly_charges = models.CharField(max_length=500,null=True, default="")
    # yearly_charges = models.CharField(max_length=500,null=True, default="")

class flagbillreason(models.Model):
    m_business_id = models.CharField(max_length=100)
    reason = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class NozzleCount(models.Model):
    business_id = models.CharField(max_length=100)
    nozzle_count = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class CompniesName(models.Model):
    m_business_id = models.CharField(max_length=100)
    company_name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class MerchantPaymentSetting(models.Model):
    m_business_id = models.CharField(max_length=100)
    payu_key = models.CharField(max_length=100,default="",null=True)
    payu_salt = models.CharField(max_length=200,default="",null=True)
    created_at = models.DateTimeField(default=timezone.now)
    upi_id = models.CharField(max_length=100,default="",null=True)
    option = models.CharField(max_length=100,default="")


