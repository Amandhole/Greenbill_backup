from django.db import models
from users.models import GreenBillUser
from django.utils import timezone

# Create your models here.
class ReferralModel(models.Model):
    recharge_amount_per_refferal = models.CharField(max_length=150, null=True, default=0)
    recharge_amount_per_referent = models.CharField(max_length=150, null=True, default=0)

class ReferralHistory(models.Model):
	referent_mobile_no = models.CharField(max_length=20, null=True, default=0)
	referral_mobile_no = models.CharField(max_length=20, null=True, default=0)
	is_referral = models.BooleanField(default=False)
	is_referent = models.BooleanField(default=False)
	earned_recharge_points = models.CharField(max_length=100, null=True, default=0)
	created_at = models.DateTimeField(default=timezone.now)


class PromotionsAmount(models.Model):
	
	offer_amount = models.CharField(max_length=20, null=True, default=0)

	coupon_amount = models.CharField(max_length=20, null=True, default=0)

	third_party_ads_belowbill_amount = models.CharField(max_length=20, null=True, default=0)

	green_bill_ads_belowbill_amount = models.CharField(max_length=20, null=True, default=0)