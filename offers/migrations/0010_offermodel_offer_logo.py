# Generated by Django 3.1.4 on 2021-07-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0009_offermodel_add_merchant_name_by_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='offermodel',
            name='offer_logo',
            field=models.ImageField(blank=True, default='', null=True, upload_to='uploads/'),
        ),
    ]
