# Generated by Django 3.1.4 on 2021-06-05 09:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('partner_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerdiasbleReasons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_reason', models.CharField(default='', max_length=50, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
