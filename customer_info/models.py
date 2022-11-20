from django.db import models
from users.models import GreenBillUser,MerchantProfile
from django.utils import timezone
# Create your models here.


class Customer_Info_Model(models.Model):
    mer_id = models.ForeignKey(GreenBillUser, related_name='merchant', null=True, on_delete=models.CASCADE)
    per_id = models.ForeignKey(GreenBillUser,related_name='partner', null=True, on_delete=models.CASCADE)
    merchant_business_id = models.ForeignKey(MerchantProfile,related_name='business_name', null=True, on_delete=models.CASCADE)
    cust_first_name = models.CharField(max_length=100, null=True, default=0)
    cust_last_lname = models.CharField(max_length=100, null=True, default=0)
    cust_email = models.EmailField(null=True, default=0)
    cust_mobile_num = models.CharField(max_length=12, null=True, default=0)
    customer_state = models.CharField(max_length=500, null=True, default='')
    customer_city = models.CharField(max_length=500, null=True, default='')
    customer_area = models.CharField(max_length=500, null=True, default=0)
    customer_pin_code = models.IntegerField(null=True, default=0)
    date_joined = models.DateTimeField(default=timezone.now)