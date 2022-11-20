# Generated by Django 3.1.4 on 2021-08-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_payment', '0002_auto_20210612_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentlinks',
            name='description',
            field=models.CharField(default='zappkode ', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='paymentlinks',
            name='email',
            field=models.CharField(default='rashmi@zappkode.com ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='paymentlinks',
            name='name',
            field=models.CharField(default='green_bill_name', max_length=200),
        ),
    ]
