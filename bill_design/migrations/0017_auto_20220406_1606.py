# Generated by Django 3.1.4 on 2022-04-06 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_design', '0016_auto_20220405_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_card',
            name='gallery1',
            field=models.ImageField(blank=True, null=True, upload_to='card_pic/'),
        ),
        migrations.AddField(
            model_name='contact_card',
            name='gallery2',
            field=models.ImageField(blank=True, null=True, upload_to='card_pic/'),
        ),
        migrations.AddField(
            model_name='contact_card',
            name='gallery3',
            field=models.ImageField(blank=True, null=True, upload_to='card_pic/'),
        ),
    ]
