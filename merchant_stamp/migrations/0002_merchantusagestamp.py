# Generated by Django 3.1.4 on 2021-07-21 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchant_stamp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='merchantusagestamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_stamp_id_one', models.CharField(max_length=50, null=True)),
                ('merchant_stamp_id_two', models.CharField(max_length=50, null=True)),
                ('merchant_user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
