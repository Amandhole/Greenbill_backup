# Generated by Django 3.1.4 on 2021-05-24 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='partner_subscriptions_keys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='partner_subscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.CharField(blank=True, max_length=500, null=True)),
                ('per_bill_cost', models.FloatField(blank=True, null=True)),
                ('digital_bill', models.FloatField(blank=True, null=True)),
                ('total_amount_avilable', models.FloatField(blank=True, null=True)),
                ('purchase_cost', models.FloatField(blank=True, null=True)),
                ('purchase_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=False, null=True)),
                ('plan_type', models.CharField(blank=True, max_length=500, null=True)),
                ('partner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='partner_recharge_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_plan_id', models.CharField(blank=True, max_length=500, null=True)),
                ('subscription_name', models.CharField(blank=True, max_length=500, null=True)),
                ('per_bill_cost', models.FloatField(blank=True, null=True)),
                ('digital_bill', models.FloatField(blank=True, null=True)),
                ('is_subscription_plan', models.BooleanField(default=False, null=True)),
                ('cost', models.FloatField(blank=True, null=True)),
                ('purchase_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('plan_type', models.CharField(blank=True, max_length=500, null=True)),
                ('partner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
