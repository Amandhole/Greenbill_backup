# Generated by Django 3.1.4 on 2022-02-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_design', '0007_auto_20211229_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_designs',
            name='indiamart',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='indiamart_url',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='justdail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='justdail_url',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
