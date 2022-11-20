from django.db import models

# Create your models here.


class availmodels(models.Model):
    lover_price = models.CharField(max_length=120, null=True)
