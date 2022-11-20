# Generated by Django 3.1.4 on 2021-03-03 07:49

import ckeditor_uploader.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='system_updates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('message', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('group_customer', models.BooleanField(default=False, null=True)),
                ('group_merchant', models.BooleanField(default=False, null=True)),
                ('group_partner', models.BooleanField(default=False, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
