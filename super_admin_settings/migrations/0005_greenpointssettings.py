# Generated by Django 3.1.4 on 2021-06-05 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin_settings', '0004_paymentsetting'),
    ]

    operations = [
        migrations.CreateModel(
            name='GreenPointsSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_points', models.CharField(max_length=100)),
                ('referral_points', models.CharField(max_length=100)),
            ],
        ),
    ]
