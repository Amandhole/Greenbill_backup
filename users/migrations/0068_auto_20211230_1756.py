# Generated by Django 3.1.4 on 2021-12-30 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0067_partnerprofile_p_commission_per_digital_marketing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partnerprofile',
            old_name='p_commission_per_digital_marketing',
            new_name='p_commission_per_other_services',
        ),
    ]