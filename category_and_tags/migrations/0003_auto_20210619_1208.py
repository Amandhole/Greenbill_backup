# Generated by Django 3.1.4 on 2021-06-19 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category_and_tags', '0002_bill_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_tags',
            name='is_customer_bill_tag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bill_tags',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
