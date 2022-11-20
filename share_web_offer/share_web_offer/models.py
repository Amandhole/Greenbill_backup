from django.db import models
from users.models import GreenBillUser, MerchantProfile
from django.utils import timezone
from datetime import date

# Create your models here.
class ShareOfferModel(models.Model):
    share_offer_image = models.ImageField(upload_to="uploads/", blank=True, null=True, default="")
    offer_url = models.CharField(max_length=200, blank=True, default='')
