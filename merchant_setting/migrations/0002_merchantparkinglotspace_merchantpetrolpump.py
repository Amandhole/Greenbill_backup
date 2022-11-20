# Generated by Django 3.1.4 on 2021-01-16 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchant_setting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantPetrolPump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_business_id', models.CharField(max_length=100)),
                ('product_id', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=100)),
                ('product_cost', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MerchantParkingLotSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_business_id', models.CharField(max_length=100)),
                ('entry_gate', models.CharField(max_length=100)),
                ('exit_gate', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(choices=[('1', '2 Wheeler'), ('2', '3 Wheeler'), ('3', '4 Wheeler')], max_length=1)),
                ('spaces', models.CharField(max_length=100)),
                ('charges_by', models.CharField(choices=[('1', 'Vehicle Type'), ('2', 'Hourly')], max_length=1)),
                ('charges', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
