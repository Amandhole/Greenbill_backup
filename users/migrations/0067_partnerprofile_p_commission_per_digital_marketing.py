# Generated by Django 3.1.4 on 2021-12-30 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0066_merchantprofile_schedule_pdf_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerprofile',
            name='p_commission_per_digital_marketing',
            field=models.CharField(blank=True, default='0', max_length=100, null=True),
        ),
    ]
