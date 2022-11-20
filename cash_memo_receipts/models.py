from django.db import models
from users.models import GreenBillUser


# Create your models here.


class Cash_Memos(models.Model):
    memo_name = models.CharField(max_length=100, null=True, default="")
    header_text = models.CharField(max_length=500, null=True, default="")
    footer_text = models.CharField(max_length=500, null=True, default="")
    stamp_image = models.ImageField(upload_to="cash_memo")
    fav_color = models.CharField(max_length=50, null=True, default="")


class Receipts_Model(models.Model):
    receipts_name = models.CharField(max_length=100, null=True, default="")
    header_text = models.CharField(max_length=500, null=True, default="")
    footer_text = models.CharField(max_length=500, null=True, default="")
    stamp_image = models.ImageField(upload_to="cash_memo")
    fav_color = models.CharField(max_length=50, null=True, default="")
