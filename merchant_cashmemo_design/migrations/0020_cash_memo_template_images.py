# Generated by Django 3.1.4 on 2021-12-14 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant_cashmemo_design', '0019_auto_20211110_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='cash_memo_template_images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_id', models.CharField(blank=True, max_length=20, null=True)),
                ('img_url', models.ImageField(blank=True, default='', null=True, upload_to='cash_receipt_images/')),
            ],
        ),
    ]
