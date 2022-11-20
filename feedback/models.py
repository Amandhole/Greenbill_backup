from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    mobile_no = models.CharField(max_length=100)
    bug =  models.BooleanField(default=False)
    suggestion = models.BooleanField(default=False)
    comments = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    is_customer = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    status = models.CharField(max_length=120, null='True')