# Generated by Django 3.1.4 on 2021-09-13 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0048_merchantprofile_schedule_pdf_upload'),
        ('merchant_stamp', '0005_merchantstampupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='selectstampimage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_select_image', models.ImageField(blank=True, default='', null=True, upload_to='merchant_business_stamp_img_upload')),
                ('merchant_business_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.merchantprofile')),
                ('merchant_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
