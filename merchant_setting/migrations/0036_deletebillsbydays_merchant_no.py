# Generated by Django 3.1.4 on 2022-01-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_setting', '0035_deletebillsbydays'),
    ]

    operations = [
        migrations.AddField(
            model_name='deletebillsbydays',
            name='merchant_no',
            field=models.CharField(default='', max_length=100),
        ),
    ]
