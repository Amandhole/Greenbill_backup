# Generated by Django 3.1.4 on 2021-04-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_setting', '0025_nozzlecount'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompniesName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_business_id', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
