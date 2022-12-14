# Generated by Django 3.1.4 on 2021-03-13 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchant_setting', '0017_parking_app_setting_model_manage_space'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantparkingspacecharges',
            name='half_yearly_charges',
        ),
        migrations.RemoveField(
            model_name='merchantparkingspacecharges',
            name='monthly_charges',
        ),
        migrations.RemoveField(
            model_name='merchantparkingspacecharges',
            name='per_visit_charges',
        ),
        migrations.RemoveField(
            model_name='merchantparkingspacecharges',
            name='quarterly_charges',
        ),
        migrations.RemoveField(
            model_name='merchantparkingspacecharges',
            name='yearly_charges',
        ),
        migrations.CreateModel(
            name='MerchantParkingLotPassCharges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_business_id', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('per_visit_charges', models.CharField(default='', max_length=500, null=True)),
                ('monthly_charges', models.CharField(default='', max_length=500, null=True)),
                ('quarterly_charges', models.CharField(default='', max_length=500, null=True)),
                ('half_yearly_charges', models.CharField(default='', max_length=500, null=True)),
                ('yearly_charges', models.CharField(default='', max_length=500, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
