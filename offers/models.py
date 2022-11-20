from django.db import models
from users.models import GreenBillUser, MerchantProfile
from django.utils import timezone
from datetime import date


class OfferModel(models.Model):
    merchant_user = models.ForeignKey(GreenBillUser, on_delete=models.CASCADE, null= True)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    offer_name=models.CharField(max_length = 150, null= True)
    offer_caption=models.CharField(max_length = 150, null= True)
    valid_from=models.DateField(null=True, blank=True)
    valid_through=models.DateField(null=True, blank=True)

    offer_image = models.ImageField(upload_to="uploads/", blank=True, null=True, default="")
    
    offer_logo = models.ImageField(upload_to="uploads/", blank=True, null=True, default="")
    disapproved_reason = models.CharField(max_length=1000, null=True, default="Not Applicable")
    status = models.CharField(max_length=100, default="0")
    Offer_type = models.CharField(max_length = 150, null= True)
    offer_business_category = models.CharField(max_length = 150, null= True)
    created_date = models.DateTimeField(default=timezone.now)
    offer_panel = models.CharField(max_length=100, default="merchant")
    o_business_name = models.CharField(max_length = 150, null= True)
    merchant_business_name = models.CharField(max_length = 150, null= True)
    check_business_category = models.CharField(max_length = 150, null= True)


    customer_city = models.CharField(max_length = 150, null= True)
    customer_state = models.CharField(max_length = 150, null= True)
    customer_area = models.CharField(max_length = 150, null= True)
    merchant_state = models.CharField(max_length = 150, null= True)
    merchant_district = models.CharField(max_length = 150, null= True)
    merchant_city = models.CharField(max_length = 150, null= True)
    merchant_area = models.CharField(max_length = 150, null= True)

    offer_amount = models.CharField(max_length = 150, null= True, default="0")
    cout = models.IntegerField(null= True, default="0")
    customer_merchant_count = models.IntegerField(null= True, default="0")

    add_merchant_name_by_owner = models.CharField(max_length = 150, null= True)

    partner_state = models.CharField(max_length = 150, null= True)
    partner_city = models.CharField(max_length = 150, null= True)
    partner_area = models.CharField(max_length = 150, null= True)


