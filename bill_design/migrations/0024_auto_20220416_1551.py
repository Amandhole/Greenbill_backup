# Generated by Django 3.1.4 on 2022-04-16 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_design', '0023_contact_card_sharecount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_card',
            name='sharecount',
            field=models.CharField(default='', max_length=10),
        ),
    ]
