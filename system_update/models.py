from django.db import models
from django.utils import timezone
from users.models import GreenBillUser
from ckeditor_uploader.fields import RichTextUploadingField

class system_updates(models.Model):
    title = models.CharField(max_length=1000)
    message = RichTextUploadingField(blank=True, null=True)
    group_customer = models.BooleanField(default=False, null=True)
    group_merchant = models.BooleanField(default=False, null=True)
    group_partner = models.BooleanField(default=False, null=True)
    group_petrol = models.BooleanField(default=False, null=True)
    group_parking = models.BooleanField(default=False, null=True)
    created_date =  models.DateTimeField(default=timezone.now)


class unread_system_updates(models.Model):
    user_id = models.CharField(max_length=20,null=True)
    notification_id =models.IntegerField(null=True)
    group_customer = models.BooleanField(default=False, null=True)
    group_merchant = models.BooleanField(default=False, null=True)
    group_partner = models.BooleanField(default=False, null=True)
    group_petrol = models.BooleanField(default=False, null=True)
    group_parking = models.BooleanField(default=False, null=True)
    read_status = models.BooleanField(default=False, null=True)
    created_date =  models.DateTimeField(default=timezone.now)