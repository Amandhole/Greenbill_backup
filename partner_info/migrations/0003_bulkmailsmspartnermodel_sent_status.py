# Generated by Django 3.1.4 on 2021-06-16 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner_info', '0002_partnerdiasblereasons'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkmailsmspartnermodel',
            name='sent_status',
            field=models.CharField(max_length=120, null=True),
        ),
    ]