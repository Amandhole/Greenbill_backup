# Generated by Django 3.1.4 on 2021-01-22 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SavePetrolPumpBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_user', models.CharField(max_length=100)),
                ('m_business_id', models.CharField(max_length=100)),
                ('c_name', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=100)),
                ('c_email', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(max_length=100)),
                ('vehicle_number', models.CharField(max_length=100)),
                ('product_id', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=100)),
                ('product_cost', models.CharField(max_length=100)),
                ('volume', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('invoice_no', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]