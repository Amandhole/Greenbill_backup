# Generated by Django 3.1.4 on 2021-07-01 05:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_auto_20210618_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantprofile',
            name='merchant_by_partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner_record', to=settings.AUTH_USER_MODEL),
        ),
    ]