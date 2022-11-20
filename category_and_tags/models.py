from django.db import models
from django.conf import settings



# Create your models here.
class business_category(models.Model):
    business_category_name = models.CharField(max_length=200, default='')
    business_category_description = models.CharField(max_length=1000, default='')

    def __str__(self): 
        return self.business_category_name

class bill_category(models.Model):
    bill_category_name = models.CharField(max_length=200, default='')
    bill_category_description = models.CharField(max_length=1000, default='')
    icon = models.ImageField(null=True, blank=True, upload_to='bill_category_icons', default="")

    def __str__(self):
        return self.bill_category_name 

class bill_tags(models.Model):
    bill_tags_name = models.CharField(max_length=200, default='')
    bill_tags_description = models.CharField(max_length=1000, default='')   

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_customer_bill_tag = models.BooleanField(default=False)


