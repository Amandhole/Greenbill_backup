# Generated by Django 3.1.4 on 2021-11-10 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_cashmemo_design', '0018_auto_20211110_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercashmemodetailmodels',
            name='rejected_reason',
            field=models.CharField(default='', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='customerreceiptdetailsmodels',
            name='rejected_reason',
            field=models.CharField(default='', max_length=120, null=True),
        ),
    ]