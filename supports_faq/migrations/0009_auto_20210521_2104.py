# Generated by Django 3.1.4 on 2021-05-21 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supports_faq', '0008_auto_20210520_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogs_model',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='faqs_model',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='video_model',
            name='created_date',
        ),
    ]
