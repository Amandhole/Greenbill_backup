# Generated by Django 3.1.4 on 2021-01-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petrol_pump_apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceNumberPetrolPump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('m_business_id', models.CharField(max_length=100)),
                ('invoice_no', models.CharField(max_length=100)),
            ],
        ),
    ]
