from django.db import models
from users.models import GreenBillUser, MerchantProfile
from datetime import datetime
from django.utils import timezone
# Create your models here.


class CouponModel(models.Model):
    merchant_id = models.ForeignKey(
        GreenBillUser, null=True, on_delete=models.CASCADE)
    merchant_business_id = models.CharField(max_length=100, null=True, default="")
    coupon_name = models.CharField(max_length=100, null=True, default="")
    valid_from = models.DateField(null=True, default="")
    valid_through = models.DateField(null=True, default="")
    coupon_code = models.CharField(max_length=100, null=True, default="")
    coupon_value = models.CharField(max_length=100, null=True, default="")
    green_point = models.CharField(max_length=100, null=True, default="")
    coupon_logo = models.ImageField(upload_to="Coupon_Logo/", null=True, default="")
    coupon_redeem = models.CharField(max_length=10, null=True, default="0")
    coupon_caption = models.CharField(max_length=50, null=True, default="")
    coupon_background_color = models.CharField(max_length=100,null=True,default="")
    coupon_valid_for_user = models.CharField(max_length=100,null=True,default="")
    amount_in = models.CharField(max_length=100,null=True,default="")

    customer_city = models.CharField(max_length = 150, null= True)
    customer_state = models.CharField(max_length = 150, null= True)
    customer_area = models.CharField(max_length = 150, null= True)
    cout = models.IntegerField(null= True, default="0")

    add_merchant_name_by_owner = models.CharField(max_length = 150, null= True)
    coupon_panel = models.CharField(max_length = 150, null= True, default="merchant")
    owner_name = models.CharField(max_length = 150, null= True)

    total_customers = models.CharField(max_length = 150, null= True, blank = True)
    created_date = models.DateTimeField(default=timezone.now)
    coupon_amount = models.CharField(max_length=100, null=True, default="0.00")
    

class RedeemCouponModel(models.Model):
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE)
    merchant_business_id = models.CharField(max_length=100, null=True, default="")
    user_id = models.CharField(max_length=100, null=True, default="")
    coupon_id = models.CharField(max_length=100, null=True, default="")
    coupon_name = models.CharField(max_length=100, null=True, default="")
    coupon_code = models.CharField(max_length=100, null=True, default="")
    green_point = models.CharField(max_length=100, null=True, default="")
    coupon_redeem_date = models.DateTimeField(default=datetime.now(),blank=True)