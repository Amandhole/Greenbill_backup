# Generated by Django 3.1.4 on 2021-07-06 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0008_auto_20210703_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='offermodel',
            name='add_merchant_name_by_owner',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
