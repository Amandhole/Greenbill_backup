from django.db import models
from users.models import *

# Create your models here.

class StampModel(models.Model):
    content = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    stampdesgn = models.CharField(max_length=50)

class merchantusagestamp(models.Model):
    merchant_user_id = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    merchant_stamp_id_one = models.CharField(max_length=50, null=True)
    merchant_stamp_id_two = models.CharField(max_length=50, null=True)
    is_check = models.CharField(max_length=50, null=True)

class merchantstampupload(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    m_business_stamp = models.ImageField(null=True, blank=True, upload_to='merchant_business_stamp', default="")
    stamp_name = models.CharField(max_length=100, default="My Stamp")

class selectstampimage(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    m_select_image = models.CharField(max_length=50, null=True)

class usecashmemostamp(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    stamp_image_id = models.CharField(max_length=50, null=True)

class usereceiptrstamp(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    stamp_image_id = models.CharField(max_length=50, null=True)







    

