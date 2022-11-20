from django.db import models
from offers.models import OfferModel
from users.models import GreenBillUser

# Create your models here.
class statusmodels(models.Model):
    offer_name = models.CharField(max_length=120, null=True)
    offer_caption = models.CharField(max_length=120, null=True)
   

    