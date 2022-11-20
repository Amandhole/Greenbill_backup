# -*- encoding: utf-8 -*-
"""
Copyright (c) 2020 - present Hind Softwares
"""

from django.contrib import admin
from django.contrib.admin.models import LogEntry
admin.site.register(LogEntry)

# Register your models here.
from .models import generalSetting, test

admin.site.register(generalSetting)
admin.site.register(test)
