# Generated by Django 3.1.4 on 2021-10-05 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_bill', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharebillmodel',
            name='user_id',
            field=models.CharField(max_length=150, null=True),
        ),
    ]