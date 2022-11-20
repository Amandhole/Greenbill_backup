from django.db import models
from django.utils import timezone

class ShareWord(models.Model):
    mobile_no = models.CharField(max_length=100)
    words = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
