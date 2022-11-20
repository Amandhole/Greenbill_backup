from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

from users.models import GreenBillUser, MerchantProfile

class merchant_role(models.Model):
    merchant_id = models.ForeignKey(GreenBillUser, null=True, on_delete = models.SET_NULL)
    role_name = models.CharField(max_length=100)
    merchant_business_id = models.ForeignKey(MerchantProfile, null=True, on_delete = models.SET_NULL, blank=True)
    role_description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.role_name

class merchant_module(models.Model):
    module_name = models.CharField(max_length=500)

    def __str__(self): 
        return self.module_name

class merchant_feature(models.Model):
    feature_id = models.CharField(max_length=500)
    module_id = models.ForeignKey(merchant_module, null=True, on_delete = models.SET_NULL)
    view = models.CharField(max_length=500, blank=True)
    add = models.CharField(max_length=500, blank=True)
    edit = models.CharField(max_length=500, blank=True)
    delete = models.CharField(max_length=500, blank=True)
    view_permission = models.CharField(max_length=500, blank=True)
    add_permission = models.CharField(max_length=500, blank=True, null=True)
    edit_permission = models.CharField(max_length=500, blank=True, null=True)
    delete_permission = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.feature_id

class merchant_permission(models.Model):
    merchant_user_id = models.ForeignKey(GreenBillUser, null=True, on_delete = models.SET_NULL)
    role_id = models.ForeignKey(merchant_role, null=True, on_delete = models.SET_NULL, blank=True)
    module_id = models.ForeignKey(merchant_module, null=True, on_delete = models.SET_NULL, blank=True)
    feature_id = models.ForeignKey(merchant_feature, null=True, on_delete = models.SET_NULL, blank=True)
    view_permission = models.CharField(max_length=500, blank=True, null=True)
    add_permission = models.CharField(max_length=500, blank=True, null=True)
    edit_permission = models.CharField(max_length=500, blank=True, null=True)
    delete_permission = models.CharField(max_length=500, blank=True, null=True)

class merchant_userrole(models.Model):
    user   = models.OneToOneField(GreenBillUser, null=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(merchant_role, null=True, on_delete = models.SET_NULL, blank=True)