# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class otp_validation(models.Model):
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    otp = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.mobile_no

class StateCityData(models.Model):
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self): 
        return self.state