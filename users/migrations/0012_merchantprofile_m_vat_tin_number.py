# Generated by Django 3.1.4 on 2021-02-13 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_partnerprofile_p_business_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantprofile',
            name='m_vat_tin_number',
            field=models.CharField(default='', max_length=100),
        ),
    ]
