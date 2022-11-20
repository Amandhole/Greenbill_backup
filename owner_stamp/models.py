from django.db import models

# Create your models here.

class wstampmodels(models.Model):
    stamp_name = models.CharField(max_length=120, null=True)
    stamp_content = models.CharField(max_length=120, null=True)
    option_color = models.CharField(max_length=120, null=True)
    selection_design = models.CharField(max_length=120, null=True)
    
class stampdmodels(models.Model):
    name = models.CharField(max_length=120, null=True) 