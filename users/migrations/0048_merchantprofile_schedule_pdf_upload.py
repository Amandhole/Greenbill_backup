# Generated by Django 3.1.4 on 2021-09-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0047_auto_20210906_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantprofile',
            name='schedule_pdf_upload',
            field=models.FileField(blank=True, default='', null=True, upload_to='payu_schedule_upload_pdf'),
        ),
    ]