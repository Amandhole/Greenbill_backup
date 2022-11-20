from django.db import models
from users.models import MerchantProfile, GreenBillUser
# Create your models here.


class MerchantEnquiryModel(models.Model):
    """
    Digital Marketing Merchant Enquiry Model
    """
    mer_id = models.ForeignKey(
        GreenBillUser, null=True, on_delete=models.CASCADE,)
    customer_name = models.CharField(max_length=50, default='', null=True)
    bissiness_name = models.CharField(max_length=50, default='', null=True)
    contact_no = models.CharField(max_length=12,)
    email_id = models.EmailField(max_length=100, default='', null=True)
    intrested_in = models.CharField(max_length=500, default='', null=True)
    comments = models.CharField(max_length=20000, default='', null=True)
    enquary_status = models.CharField(
        max_length=15, default="Active", null=True)
    read_status = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=100, null=True)
    assign_company = models.CharField(max_length=100, null=True)
    notes = models.CharField(max_length=100, null=True)


