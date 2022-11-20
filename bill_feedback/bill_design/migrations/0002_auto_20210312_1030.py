# Generated by Django 3.1.4 on 2021-03-12 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_design', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_designs',
            name='android',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='android_url',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='google',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='google_url',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='linkedin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='linkedin_url',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='pinterest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='pinterest_url',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='skype',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='skype_url',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='snapchat',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_designs',
            name='snapchat_url',
            field=models.CharField(default='', max_length=1000),
        ),
    ]