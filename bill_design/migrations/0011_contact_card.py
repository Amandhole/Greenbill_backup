# Generated by Django 3.1.4 on 2022-03-25 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0071_merchantprofile_loyalty_point'),
        ('bill_design', '0010_auto_20220323_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact_card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_name', models.CharField(max_length=45, null=True)),
                ('card_phone_no', models.CharField(max_length=45, null=True)),
                ('card_email', models.CharField(max_length=45, null=True)),
                ('card_country', models.CharField(max_length=45, null=True)),
                ('card_city', models.CharField(max_length=45, null=True)),
                ('card_photo', models.FileField(blank=True, null=True, upload_to='card_pic')),
                ('facebook', models.BooleanField(default=False)),
                ('facebook_url', models.CharField(default='', max_length=1000)),
                ('youtube', models.BooleanField(default=False)),
                ('youtube_url', models.CharField(default='', max_length=1000)),
                ('phone', models.BooleanField(default=False)),
                ('phone_number', models.CharField(default='', max_length=100)),
                ('website', models.BooleanField(default=False)),
                ('website_url', models.CharField(default='', max_length=1000)),
                ('map', models.BooleanField(default=False)),
                ('map_link', models.CharField(default='', max_length=1000)),
                ('merchant_business_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.merchantprofile')),
            ],
        ),
    ]
