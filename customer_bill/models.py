from django.db import models
from users.models import GreenBillUser
from category_and_tags.models import bill_category
from users.models import MerchantProfile
# Create your models here.


# class Customer_Bill_Customer_Added(models.Model):
#     cust_id = models.ForeignKey(
#         GreenBillUser, null=True, on_delete=models.CASCADE,)
#     cust_bill = models.FileField(
#         upload_to="Customer_Bill/", default="", null=True)
#     business_name = models.ForeignKey(MerchantProfile, default='', on_delete=models.CASCADE, blank=True, null=True)
#     customer_bill_category = models.ForeignKey(bill_category, default='', on_delete=models.CASCADE, blank=True, null=True)
#     bill_amount = models.FloatField(default="", null=True)
#     bill_date = models.DateField(default="", null=True)


class Sharebillmodel(models.Model):
	user_id=models.CharField(max_length = 150, null= True)
	mobile_no=models.CharField(max_length = 150, null= True)
	db_table=models.CharField(max_length = 150, null= True)
	bill_id=models.CharField(max_length = 150, null= True)

