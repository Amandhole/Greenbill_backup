# Generated by Django 3.1.4 on 2021-06-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner_bill_design', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill_designs_owner',
            name='address',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
