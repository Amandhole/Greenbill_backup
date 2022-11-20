from django.db import models
from users.models import GreenBillUser

class GreenPointsModel(models.Model):
    mobile_no = models.CharField(null=True, max_length = 20)
    green_points_count = models.CharField(max_length=100, blank=True, null=True, default='')