# Generated by Django 3.1.4 on 2021-12-21 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_stamp', '0010_delete_merchant_receipt_upload_stamp_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantstampupload',
            name='stamp_name',
            field=models.CharField(default='My Stamp', max_length=100),
        ),
    ]
