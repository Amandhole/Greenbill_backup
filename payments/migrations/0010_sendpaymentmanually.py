# Generated by Django 3.1.4 on 2021-11-16 10:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_auto_20211024_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendPaymentManually',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_id', models.CharField(max_length=20)),
                ('partner_id', models.CharField(max_length=20)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('payu_transaction_id', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('payment_mode', models.CharField(max_length=100, null=True)),
                ('amount', models.CharField(max_length=100, null=True)),
                ('payment_for', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]