# Generated by Django 3.1.4 on 2020-12-31 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_greenbilluser_c_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantprofile',
            name='m_area',
            field=models.CharField(default='', max_length=500, null=True),
        ),
    ]
