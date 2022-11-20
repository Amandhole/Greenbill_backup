from django.db import models
from users.models import GreenBillUser, MerchantProfile
from datetime import datetime
# Create your models here.


class OwnerCouponModel(models.Model):
    owner_id = models.ForeignKey(
        GreenBillUser, null=True, on_delete=models.CASCADE)
    merchant_business_id = models.CharField(max_length=100, null=True, default="")
    coupon_name = models.CharField(max_length=100, null=True, default="")
    valid_from = models.DateField(null=True, default="")
    valid_through = models.DateField(null=True, default="")
    coupon_code = models.CharField(max_length=100, null=True, default="")
    coupon_value = models.CharField(max_length=100, null=True, default="")
    green_point = models.CharField(max_length=100, null=True, default="")
    # coupon_logo = models.ImageField(upload_to="Coupon_Logo/", null=True, default="")
    coupon_redeem = models.CharField(max_length=10, null=True, default="0")
    coupon_caption = models.CharField(max_length=50, null=True, default="")
    coupon_background_color = models.CharField(max_length=100,null=True,default="")
    coupon_valid_for_user = models.CharField(max_length=100,null=True,default="")
    amount_in = models.CharField(max_length=100,null=True,default="")
    customer_city = models.CharField(max_length = 150, null= True)
    customer_state = models.CharField(max_length = 150, null= True)
    customer_area = models.CharField(max_length = 150, null= True)

    add_merchant_name_by_owner = models.CharField(max_length = 150, null= True)

class RedeemOwnerCouponModel(models.Model):
    owner_id = models.ForeignKey(GreenBillUser, null=True, on_delete=models.CASCADE)
    merchant_business_id = models.CharField(max_length=100, null=True, default="")
    user_id = models.CharField(max_length=100, null=True, default="")
    coupon_id = models.CharField(max_length=100, null=True, default="")
    coupon_name = models.CharField(max_length=100, null=True, default="")
    coupon_code = models.CharField(max_length=100, null=True, default="")
    green_point = models.CharField(max_length=100, null=True, default="")
    coupon_redeem_date = models.DateTimeField(default=datetime.now(),blank=True)