# Generated by Django 3.1.4 on 2021-07-01 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_auto_20210701_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='merchantuniqueids',
            old_name='m_unique_id',
            new_name='m_unique_no',
        ),
        migrations.RenameField(
            model_name='partneruniqueids',
            old_name='p_unique_id',
            new_name='p_unique_no',
        ),
    ]
