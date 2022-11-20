# Generated by Django 3.1.4 on 2021-05-27 10:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_setting', '0032_auto_20210412_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantPaymentSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_business_id', models.CharField(max_length=100)),
                ('payu_key', models.CharField(max_length=100)),
                ('payu_salt', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
