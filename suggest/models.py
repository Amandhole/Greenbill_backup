from django.db import models
from django.utils import timezone

class SuggestBusiness(models.Model):
    m_business_id = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    suggested_business_name = models.CharField(max_length=1000, null=True, blank=True)
    contact_no = models.IntegerField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    is_parking = models.BooleanField(default=False, null=True)
    is_petrol = models.BooleanField(default=False, null=True)
    is_other = models.BooleanField(default=False, null=True)
    created_at =  models.DateTimeField(default=timezone.now)