from django.db import models
from django.utils import timezone

# Create your models here.


class SavePetrolPumpBill(models.Model):
    user_id = models.CharField(max_length=100, blank=True)
    m_user_id = models.CharField(max_length=100, blank=True)
    m_business_id = models.CharField(max_length=100, null=True)
    p_business_id = models.CharField(max_length=100, null=True)
    mobile_no = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_cost = models.CharField(max_length=100)
    volume = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    date = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    invoice_no = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    worker_name = models.CharField(max_length=100, blank=True, null=True)
    c_unique_id = models.CharField(max_length=20, null=True, default='')
    bill_file = models.ImageField(null=True, blank=True, upload_to='customer_bill', default="")
    bill_url = models.CharField(max_length=200, blank=True, default='')
    addon_product_id = models.CharField(max_length=200, blank=True, null=True)
    addon_product_name = models.CharField(max_length=200, blank=True, null=True)
    addon_product_cost = models.CharField(max_length=200, blank=True, null=True)
    total_amount = models.CharField(max_length=200, default="0")
    bill_category_id = models.CharField(max_length=100, default="26", null=True,blank=True)
    bill_tags = models.CharField(max_length=20000, blank=True, null=True, default='')
    remarks = models.CharField(max_length=200, blank=True, default='')
    addon_quantity = models.CharField(max_length=200, blank=True, default='')
    nozzle_name = models.CharField(max_length=200, blank=True, default='')
    bill_flag = models.BooleanField(default=False)
    rating = models.CharField(max_length=10, blank=True, default='')
    is_checkoutpin = models.BooleanField(default=False)
    flag_update_at = models.DateTimeField(default=timezone.now)
    flag_by = models.CharField(max_length=200, blank=True)
    reason_id = models.CharField(max_length=100, blank=True)
    reason = models.CharField(max_length=500, blank=True)
    # green_points_earned = models.CharField(max_length=500, default="1")
    green_points_earned = models.CharField(max_length=10, null=True, blank=True)
    seen_status = models.BooleanField(default=False)
    reject_status = models.BooleanField(default=False)
    reject_reason = models.CharField(max_length=500, blank=True, default='')
    payment_done = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)
    payu_transaction_id = models.CharField(max_length=100, null=True)
    is_deleted = models.BooleanField(default=False)
    is_favourite = models.BooleanField(default=False)
    greenbill_digital_bill = models.CharField(max_length=1000, blank=True, default='')
    greenbill_sms_bill = models.CharField(max_length=1000, blank=True, default='')
    delete_bill = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()


class InvoiceNumberPetrolPump(models.Model):
    user_id = models.CharField(max_length=100, blank=True)
    m_user_id = models.CharField(max_length=100, blank=True)
    m_business_id = models.CharField(max_length=100)
    invoice_no = models.CharField(max_length=100)


class PetrolLog(models.Model):
    user_id = models.CharField(max_length=100, blank=True)
    login_at = models.DateTimeField(default=timezone.now)
    logout_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)