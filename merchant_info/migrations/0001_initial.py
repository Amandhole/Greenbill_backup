# Generated by Django 2.2.10 on 2020-11-06 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchantName', models.CharField(max_length=100)),
                ('merchantDesc', models.CharField(max_length=200)),
            ],
        ),
    ]