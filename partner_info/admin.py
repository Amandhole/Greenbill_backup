from django.contrib import admin

# Register your models here.
from .models import bulkMailSmsPartnerModel, PartnerMonthlyCommision, csvfileupload, SampleExcelFile

admin.site.register(bulkMailSmsPartnerModel)

admin.site.register(PartnerMonthlyCommision)

admin.site.register(csvfileupload)

admin.site.register(SampleExcelFile)
