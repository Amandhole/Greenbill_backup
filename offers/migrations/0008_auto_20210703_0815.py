# Generated by Django 3.1.4 on 2021-07-03 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0007_auto_20210702_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='offermodel',
            name='customer_area',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='offermodel',
            name='customer_state',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
