# Generated by Django 3.1.4 on 2022-03-31 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_design', '0014_auto_20220328_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_pdf_check',
            name='image_con',
            field=models.FileField(blank=True, null=True, upload_to='temp1/'),
        ),
        migrations.AlterField(
            model_name='temp_pdf_check',
            name='pdf_image',
            field=models.FileField(blank=True, null=True, upload_to='temp1/'),
        ),
    ]