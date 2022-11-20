# Generated by Django 3.1.4 on 2021-08-27 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral_points', '0003_auto_20210605_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionsAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_amount', models.CharField(default=0, max_length=20, null=True)),
                ('coupon_amount', models.CharField(default=0, max_length=20, null=True)),
                ('third_party_ads_belowbill_amount', models.CharField(default=0, max_length=20, null=True)),
                ('green_bill_ads_belowbill_amount', models.CharField(default=0, max_length=20, null=True)),
            ],
        ),
    ]