# Generated by Django 3.1.4 on 2021-10-29 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0058_auto_20211029_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantprofile',
            name='schedule_pdf_upload',
            field=models.FileField(blank=True, default='', null=True, upload_to='payu_schedule_upload_pdf'),
        ),
    ]
