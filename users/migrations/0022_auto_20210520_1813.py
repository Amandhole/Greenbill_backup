# Generated by Django 3.1.4 on 2021-05-20 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_partner_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantprofile',
            name='m_disabled_account',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='partnerprofile',
            name='p_disabled_account',
            field=models.BooleanField(default=True),
        ),
    ]
