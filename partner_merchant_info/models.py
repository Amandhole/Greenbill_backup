from django.db import models

# Create your models here.

class partnermodels(models.Model):
    my_partner = models.CharField(max_length=120, null=True)