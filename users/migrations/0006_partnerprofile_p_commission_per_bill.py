# Generated by Django 3.1.4 on 2021-01-19 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_partnercategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerprofile',
            name='p_commission_per_bill',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
