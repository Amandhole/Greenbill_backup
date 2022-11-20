# Generated by Django 3.1.4 on 2021-06-17 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_merchantprofile_by_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantprofile',
            name='merchant_by_partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner_record', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='merchantprofile',
            name='m_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_record', to=settings.AUTH_USER_MODEL),
        ),
    ]