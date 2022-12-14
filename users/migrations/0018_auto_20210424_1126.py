# Generated by Django 3.1.4 on 2021-04-24 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210327_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantprofile',
            name='m_aadhaar_number',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='partnerprofile',
            name='p_aadhaar_number',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='partnerprofile',
            name='p_active_account',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='partnerprofile',
            name='p_area',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='partnerprofile',
            name='p_cancelled_cheque_certificate',
            field=models.ImageField(blank=True, default='', null=True, upload_to='cancel_bank_cheque_photo'),
        ),
        migrations.AddField(
            model_name='partnerprofile',
            name='p_udyog_adhar_certificate',
            field=models.ImageField(blank=True, default='', null=True, upload_to='other_document_certificate1'),
        ),
        migrations.AddField(
            model_name='partnerprofile',
            name='p_vat_tin_number',
            field=models.CharField(default='', max_length=100),
        ),
    ]
