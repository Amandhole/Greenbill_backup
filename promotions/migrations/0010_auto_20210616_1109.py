# Generated by Django 3.1.4 on 2021-06-16 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0009_auto_20210609_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkmailsmsmodel',
            name='promotional',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='bulkmailsmsmodel',
            name='transactional',
            field=models.CharField(max_length=20, null=True),
        ),
    ]