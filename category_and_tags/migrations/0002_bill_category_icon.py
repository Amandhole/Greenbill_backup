# Generated by Django 3.1.4 on 2021-05-14 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_and_tags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_category',
            name='icon',
            field=models.ImageField(blank=True, default='', null=True, upload_to='bill_category_icons'),
        ),
    ]
