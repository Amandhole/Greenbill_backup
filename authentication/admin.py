# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.contrib import admin 

from .models import otp_validation, StateCityData

admin.site.register(otp_validation)

admin.site.register(StateCityData)
