# Generated by Django 3.1.4 on 2021-06-15 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchant_promotion', '0002_bulkmailsmsmerchantcustomermodel_receiver_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='templateContentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200, null=True)),
                ('template_content', models.CharField(max_length=200, null=True)),
                ('request_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='smsHeaderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200, null=True)),
                ('header_content', models.CharField(max_length=12, null=True)),
                ('request_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
