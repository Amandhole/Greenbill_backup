from django.db import models
from django.utils import timezone

class SuggestBrand(models.Model):
    mobile_no = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    brand = models.CharField(max_length=500)
    location = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    is_customer = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)