# Generated by Django 3.1.4 on 2020-12-10 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='otp_validation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True)),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
