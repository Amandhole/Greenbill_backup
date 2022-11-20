from tempfile import template
from django.core.mail import message
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from users.models import GreenBillUser, MerchantProfile
from ckeditor_uploader.fields import RichTextUploadingField

class ads_below_bill(models.Model):
    merchant = models.ForeignKey(GreenBillUser, null=True, on_delete = models.SET_NULL, blank=True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    ads_type = models.CharField(max_length=100)
    ads_name = models.CharField(max_length=100)
    redirect_url = models.CharField(max_length=500, blank=True, null=True)
    default_ads = models.BooleanField(default=False, null=True)
    business_name_value = models.CharField(max_length=2000)
    ads_image = models.ImageField(null=True, blank=True, upload_to='ads_images', default="")
    ads_image_two = models.FileField(upload_to="ads_images", null=True, blank=True)
    ads_image_three = models.FileField(upload_to="ads_images", null=True, blank=True)
    ads_image_four = models.FileField(upload_to="ads_images", null=True, blank=True)
    status = models.CharField(max_length=100, default="0")
    # status = 1 Approved
    # status = 0 Waiting for Approval
    # status = 2 Disapproved
    disapproved_reason = models.CharField(max_length=1000, default="")
    active_ads = models.BooleanField(default=False, null=True)
    created_date =  models.DateTimeField(default=timezone.now)
    start_date = models.CharField(max_length=1000, blank= True, null = True)
    end_date = models.CharField(max_length=1000, blank= True, null = True)
    days = models.CharField(max_length=1000, blank= True, null = True)
    schedule = models.BooleanField(default=False, null=True)
    ads_for = models.CharField(max_length=1000, blank= True, null = True)
    merchant_business_name = models.CharField(max_length=1000, blank= True, null = True)
    m_first_name = models.CharField(max_length=1000, blank= True, null = True)
    m_last_name = models.CharField(max_length=1000, blank= True, null = True)
    count = models.IntegerField(null= True, default="0")
    third_party_amount = models.CharField(max_length = 150, null= True, default="0")
    third_party_total_transaction = models.CharField(max_length = 150, null= True, default="0")

    received_cash_date = models.CharField(max_length=1000, blank= True, null = True)
    take_space = models.BooleanField(default=False, null=True)
    payment_done = models.BooleanField(default=False, null=True)
    approved_status = models.CharField(max_length=1000, blank= True, null = True)
    payment_amount = models.CharField(max_length=1000, blank= True, null = True)
    transaction_id = models.CharField(max_length=1000, blank= True, null = True)
    payu_transaction_id = models.CharField(max_length=1000, blank= True, null = True)
    payment_date = models.DateTimeField(null=True, blank=True)
    clicks = models.IntegerField(null= True, default="0")
    ads_below_bill_amount = models.CharField(max_length=100,default="0.00")


class ads_for_merchants(models.Model):
    ads_type = models.CharField(max_length=100)
    ads_name = models.CharField(max_length=100)
    redirect_url = models.CharField(max_length=500, blank=True, null=True)
    ads_image = models.ImageField(null=True, blank=True, upload_to='ads_images', default="")
    active_ads = models.BooleanField(default=False, null=True)
    merchants_name_value = models.CharField(max_length=2000)
    business_category_value = models.CharField(max_length=2000, null=True, default="")
    business_name_value = models.CharField(max_length=2000, null=True)
    schedule = models.BooleanField(default=False, null=True)
    start_date = models.CharField(max_length=1000, blank= True, null = True)
    end_date = models.CharField(max_length=1000, blank= True, null = True)
    created_date =  models.DateTimeField(default=timezone.now)
    days = models.CharField(max_length=1000, blank= True, null = True)
    ads_for = models.CharField(max_length=1000, blank= True, null = True)


class ads_for_green_bills(models.Model):
    # merchant = models.ForeignKey(GreenBillUser, null=True, on_delete = models.SET_NULL, blank=True)
    # merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    ads_name = models.CharField(max_length=100)
    redirect_url = models.CharField(max_length=500, blank=True, null=True)
    ads_image = models.ImageField(null=True, blank=True, upload_to='ads_images', default="")
    ads_image_two = models.FileField(upload_to="ads_images", null=True, blank=True)
    ads_image_three = models.FileField(upload_to="ads_images", null=True, blank=True)
    ads_image_four = models.FileField(upload_to="ads_images", null=True, blank=True)
    active_ads = models.BooleanField(default=False, null=True)
    created_date =  models.DateTimeField(default=timezone.now)
    merchants_name_value = models.CharField(max_length=2000, null=True)
    business_category_value = models.CharField(max_length=2000, null=True, default="")
    business_name_value = models.CharField(max_length=2000, null=True)
    start_date = models.CharField(max_length=1000, blank= True, null = True)
    end_date = models.CharField(max_length=1000, blank= True, null = True)
    schedule = models.BooleanField(default=False, null=True)
    days = models.CharField(max_length=1000, blank= True, null = True)
    ads_for = models.CharField(max_length=1000, blank= True, null = True)
    ads_type = models.CharField(max_length=100, null=True)
    m_first_name = models.CharField(max_length=1000, blank= True, null = True)
    m_last_name = models.CharField(max_length=1000, blank= True, null = True)
    count = models.IntegerField(null= True, default="0")
    clicks = models.IntegerField(null= True, default="0")



class bulkMailSmsModel(models.Model):
    owner_id = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null=True)
    receiver = models.CharField(max_length=200, null=True)
    smsheader = models.CharField(max_length=50, null=True)
    template = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=200, null=True)
    message = RichTextUploadingField(null=True)
    o_sent_sms = models.BooleanField(null=True, default="0")
    o_sent_mail = models.BooleanField(null=True, default="0")
    created_at = models.DateTimeField(default=timezone.now)
    receiver_name = models.CharField(max_length=20,null=True)
    transactional = models.CharField(max_length=20, null=True)
    promotional = models.CharField(max_length=20, null=True)
    campaign_name = models.CharField(max_length=500, default="Testing Campaign")

class bulkMailSmsSent(models.Model):
    message_id = models.ForeignKey(bulkMailSmsModel, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null=True)
    read_status = models.CharField(max_length=5, null=True,default="0")
    sent_sms = models.BooleanField(null=True, default="0")
    sent_mail = models.BooleanField(null=True, default="0")
    sent_date = models.DateTimeField(default=timezone.now)

class ads_below_bills_keys(models.Model):
    key = models.CharField(blank=True, null=True, max_length = 1000)
    created_at = models.DateTimeField(default=timezone.now)

class PromotionsPaymentHistory(models.Model):
    merchant = models.ForeignKey(GreenBillUser, null=True, on_delete = models.SET_NULL, blank=True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    ads_id = models.CharField(max_length=1000, blank= True, null = True)
    payment_amount = models.CharField(max_length=1000, blank= True, null = True)
    transaction_id = models.CharField(max_length=1000, blank= True, null = True)
    payu_transaction_id = models.CharField(max_length=1000, blank= True, null = True)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_done = models.BooleanField(default=False, null=True)


