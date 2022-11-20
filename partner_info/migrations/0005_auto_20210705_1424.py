# Generated by Django 3.1.4 on 2021-07-05 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_info', '0004_bulkmailsmspartnermodel_transactional'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkmailsmspartnermodel',
            name='customer_area',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='bulkmailsmspartnermodel',
            name='customer_city',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='bulkmailsmspartnermodel',
            name='customer_state',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
