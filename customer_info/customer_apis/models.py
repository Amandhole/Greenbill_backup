from django.db import models
from django.utils import timezone

# Create your models here.

class customerQR(models.Model):
    user_id = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)