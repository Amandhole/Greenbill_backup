# Generated by Django 3.1.4 on 2021-06-07 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_promotion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkmailsmsmerchantcustomermodel',
            name='receiver_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]