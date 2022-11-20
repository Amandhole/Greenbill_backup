from django.db import models
from django.utils import timezone
from users.models import *

# Create your models here.

class customerQR(models.Model):
    user_id = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    vehicle_no = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class Loyeltypoints(models.Model):
    mobile_no = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    loyeltyPoints = models.CharField(max_length=100, null=True)   