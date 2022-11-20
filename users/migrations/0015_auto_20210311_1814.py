# Generated by Django 3.1.4 on 2021-03-11 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_merchantprofile_m_cancel_bank_cheque_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantprofile',
            name='m_other_document1',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='merchantprofile',
            name='m_other_document2',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='merchantprofile',
            name='m_other_document_certificate1',
            field=models.ImageField(blank=True, default='', null=True, upload_to='other_document_certificate1'),
        ),
        migrations.AddField(
            model_name='merchantprofile',
            name='m_other_document_certificate2',
            field=models.ImageField(blank=True, default='', null=True, upload_to='other_document_certificate2'),
        ),
    ]
