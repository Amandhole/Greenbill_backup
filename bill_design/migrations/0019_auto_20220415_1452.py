# Generated by Django 3.1.4 on 2022-04-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_design', '0018_auto_20220412_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_card',
            name='comment',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact_card',
            name='rating',
            field=models.CharField(default='', max_length=5),
        ),
    ]
