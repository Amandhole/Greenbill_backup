# Generated by Django 3.1.5 on 2021-03-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_cashmemo_design', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cash_memo_design_model',
            name='read_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]