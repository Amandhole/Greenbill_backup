from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

class email_templates(models.Model):
    templates = RichTextUploadingField(blank=True, null=True)

class notification_settings(models.Model):
    event = models.CharField(blank = False, max_length = 500)
    message = RichTextUploadingField(blank=True, null=True)
    is_super_admin_setting = models.BooleanField(default=False)
    is_customer_setting = models.BooleanField(default=False)
    is_merchant_setting = models.BooleanField(default=False)
    is_partner_setting = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False, null=True)
    send_email = models.BooleanField(default=False, null=True)
    send_app_notification = models.BooleanField(default=False, null=True)
    is_sms = models.BooleanField(default=False, null=True)
    is_email = models.BooleanField(default=False, null=True)
    is_app_notification = models.BooleanField(default=False, null=True)

class sms_setting(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    sender_id = models.CharField(max_length=100)
    status = models.BooleanField(default=0)

class PaymentSetting(models.Model):
    payu_key = models.CharField(max_length=100, null=False)
    payu_salt = models.CharField(max_length=200, null=False)

class GreenPointsSettings(models.Model):
    bill_points = models.CharField(max_length = 100)
    referral_points = models.CharField(max_length = 100)

class GreenPointsEarnedHistory(models.Model):
    mobile_no = models.CharField(max_length=20, null=True, default=0)
    referent_mobile_no = models.CharField(max_length=20, null=True, default=0)
    referral_mobile_no = models.CharField(max_length=20, null=True, default=0)
    is_referral = models.BooleanField(default=False)
    is_referent = models.BooleanField(default=False)
    earned_green_points = models.CharField(max_length=100, null=True, default=0)
    created_at = models.DateTimeField(default=timezone.now)

class ManageCompaniesDMR(models.Model):
    comp_name = models.CharField(max_length=50, null=True)