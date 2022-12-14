# Generated by Django 3.1.4 on 2021-09-10 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0048_merchantprofile_schedule_pdf_upload'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchant_cashmemo_design', '0012_cash_memo_design_model_merchant_business_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='save_stamp_for_cashmemo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stamp_id_cashmemo', models.CharField(max_length=150, null=True)),
                ('merchant_business_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.merchantprofile')),
                ('merchant_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
