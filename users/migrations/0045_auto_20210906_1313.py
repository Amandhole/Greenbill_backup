# Generated by Django 3.1.4 on 2021-09-06 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0044_auto_20210906_1226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='merchantprofile',
            old_name='m_bank_adress',
            new_name='m_bank_adress_account',
        ),
        migrations.RenameField(
            model_name='merchantprofile',
            old_name='m_bank_entity',
            new_name='m_bank_entity_account',
        ),
    ]
