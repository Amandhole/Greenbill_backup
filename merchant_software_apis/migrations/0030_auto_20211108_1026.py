# Generated by Django 3.1.4 on 2021-11-08 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_software_apis', '0029_customerbill_table_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='extra_add',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='customerbill',
            name='is_hebrone',
            field=models.BooleanField(default=False),
        ),
    ]