# Generated by Django 3.1.4 on 2021-10-23 14:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0022_auto_20211023_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='ads_below_bills_keys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
