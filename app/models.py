# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.db import models

# Create your models here.

class emailSetting(models.Model):
    email_type = models.CharField(max_length=100, null=True)
    smtp_username = models.CharField(max_length=100, null=True)
    smtp_password = models.CharField(max_length=100, null=True)
    smtp_server = models.CharField(max_length=100, null=True)
    smtp_port = models.CharField(max_length=100, null=True)
    smtp_security = models.CharField(max_length=100, null=True)

class generalSetting(models.Model):
    user_id = models.CharField(max_length=100,default='', null=True)
    business_name = models.CharField(max_length=100,default='', null=True)
    business_code = models.CharField(max_length=50, default='',null=True)
    mobile_no = models.CharField(max_length=10, default='',null=True)
    alternate_mobile_number = models.CharField(max_length=10, default='',null=True)
    email = models.EmailField(max_length=100, null=True)
    alternate_email = models.EmailField(max_length=50, null=True)
    address = models.CharField(max_length=100,default='', null=True)
    city = models.CharField(max_length=100,default='', null=True)
    area = models.CharField(max_length=100,default='', null=True)
    district = models.CharField(max_length=100,default='', null=True)
    state = models.CharField(max_length=100,default='', null=True)
    pin_code = models.CharField(max_length=100,default='', null=True)
    pan_number = models.CharField(max_length=100,default='', null=True)
    aadhaar_number = models.CharField(max_length=100,default='', null=True)
    gstin = models.CharField(max_length=100,default='', null=True)
    cin = models.CharField(max_length=100,default='', null=True)
    tin_vat_number = models.CharField(max_length=100,default='', null=True)
    bank_account_number = models.CharField(max_length=100,default='', null=True)
    bank_IFSC_code = models.CharField(max_length=100,default='', null=True)
    bank_name = models.CharField(max_length=100,default='', null=True)
    bank_branch = models.CharField(max_length=100,default='', null=True)
    cancelled_cheque_certificate = models.FileField(null=True, blank=True, upload_to='owner_cancelled_cheque_certificate', default="")
    GSTIN_certificate = models.FileField(null=True, blank=True, upload_to='owner_GSTIN_certificate', default="")
    CIN_certificate = models.FileField(null=True, blank=True, upload_to='owner_CIN_certificate', default="")
    udyog_adhar_certificate = models.FileField(null=True, blank=True, upload_to='owner_udyog_adhar_certificate', default="")
    address_proof =  models.FileField(null=True,blank=True, upload_to='owner_address_proof', default="")
    date_format = models.CharField(max_length=100, null=True)
    currency = models.CharField(max_length=10, null=True)
    android_app_url = models.CharField(max_length=100, null=True)
    iphone_app_url = models.CharField(max_length=100, null=True)
    o_business_logo = models.ImageField(null=True, blank=True, upload_to='business_logos', default="")
    o_digital_signature = models.ImageField(null=True, blank=True, upload_to='digital_signature', default="")
    o_business_stamp = models.ImageField(null=True, blank=True, upload_to='business_stamp', default="")

class test(models.Model):
    name = models.CharField(max_length=100, null=True)