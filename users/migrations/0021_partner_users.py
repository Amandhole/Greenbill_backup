# Generated by Django 3.1.4 on 2021-05-20 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20210519_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner_users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_password', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('p_business_id', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('p_business_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('partner_user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]