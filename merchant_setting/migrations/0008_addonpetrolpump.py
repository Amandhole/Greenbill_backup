# Generated by Django 3.1.4 on 2021-02-11 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchant_setting', '0007_auto_20210208_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddonPetrolPump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_business_id', models.CharField(max_length=100)),
                ('product_id', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=100)),
                ('product_cost', models.CharField(max_length=100)),
                ('product_availability', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
