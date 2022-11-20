from django.db import models
from users.models import GreenBillUser, MerchantProfile
from django.utils import timezone
from datetime import date

# Create your models here.
class ShareOfferModel(models.Model):
    merchant = models.ForeignKey(GreenBillUser, null=True, on_delete = models.SET_NULL, blank=True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    share_offer_image = models.ImageField(upload_to="uploads/", blank=True, null=True, default="")
    offer_url = models.CharField(max_length=200, blank=True, default='')
    active_web_offer = models.BooleanField(default=False, null=True)
