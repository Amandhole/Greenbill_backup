from django.db import models
from django.utils import timezone

class bill_feedback_question(models.Model):
    merchant_business_id = models.CharField(max_length=200, default='')
    for_rating = models.CharField(max_length=10, default='') # 1 2 3 4 5
    question = models.CharField(max_length=1000, default='')
    option_1 = models.CharField(max_length=500, default='')
    option_2 = models.CharField(max_length=500, default='')
    option_3 = models.CharField(max_length=500, default='')
    created_at = models.DateTimeField(default=timezone.now, null=True,)