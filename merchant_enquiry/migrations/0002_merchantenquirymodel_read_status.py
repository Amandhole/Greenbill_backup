# Generated by Django 3.1.4 on 2021-01-20 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_enquiry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantenquirymodel',
            name='read_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
