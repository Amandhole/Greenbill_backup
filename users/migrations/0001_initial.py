# Generated by Django 3.1.4 on 2020-12-10 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('category_and_tags', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='GreenBillUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('mobile_no', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=200)),
                ('last_name', models.CharField(blank=True, default='', max_length=200)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_customer', models.BooleanField(default=False)),
                ('is_merchant', models.BooleanField(default=False)),
                ('is_partner', models.BooleanField(default=False)),
                ('is_merchant_staff', models.BooleanField(default=False)),
                ('c_email', models.EmailField(blank=True, default='', max_length=254)),
                ('c_dob', models.DateField(blank=True, null=True)),
                ('c_gender', models.CharField(max_length=10, null=True)),
                ('c_address_1', models.CharField(default='', max_length=200, null=True)),
                ('c_address_2', models.CharField(default='', max_length=200, null=True)),
                ('c_state', models.CharField(default='', max_length=100, null=True)),
                ('c_area', models.CharField(default='', max_length=500, null=True)),
                ('c_pincode', models.CharField(default='', max_length=100, null=True)),
                ('m_email', models.EmailField(blank=True, default='', max_length=254)),
                ('m_designation', models.CharField(default='', max_length=100)),
                ('m_adhaar_number', models.CharField(default='', max_length=100)),
                ('m_pan_number', models.CharField(default='', max_length=100)),
                ('m_dob', models.DateField(blank=True, null=True)),
                ('p_email', models.EmailField(blank=True, default='', max_length=254)),
                ('p_designation', models.CharField(default='', max_length=100)),
                ('p_adhaar_number', models.CharField(default='', max_length=100)),
                ('p_pan_number', models.CharField(default='', max_length=100)),
                ('p_dob', models.DateField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfileImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, default='', null=True, upload_to='profile_pic')),
                ('c_profile_image', models.ImageField(blank=True, default='', null=True, upload_to='profile_pic')),
                ('m_profile_image', models.ImageField(blank=True, default='', null=True, upload_to='profile_pic')),
                ('p_profile_image', models.ImageField(blank=True, default='', null=True, upload_to='profile_pic')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_business_name', models.CharField(default='', max_length=500)),
                ('p_pin_code', models.CharField(default='', max_length=20)),
                ('p_city', models.CharField(default='', max_length=500)),
                ('p_district', models.CharField(default='', max_length=500)),
                ('p_state', models.CharField(default='', max_length=500)),
                ('p_address', models.CharField(default='', max_length=1000)),
                ('p_landline_number', models.CharField(default='', max_length=20)),
                ('p_alternate_mobile_number', models.CharField(default='', max_length=20)),
                ('p_company_email', models.EmailField(blank=True, default='', max_length=254)),
                ('p_alternate_email', models.EmailField(blank=True, default='', max_length=254)),
                ('p_pan_number', models.CharField(default='', max_length=50)),
                ('p_gstin', models.CharField(default='', max_length=100)),
                ('p_GSTIN_certificate', models.FileField(blank=True, default='', null=True, upload_to='partner_GSTIN_certificate')),
                ('p_cin', models.CharField(default='', max_length=100)),
                ('p_CIN_certificate', models.FileField(blank=True, default='', null=True, upload_to='partner_CIN_certificate')),
                ('p_bank_account_number', models.CharField(default='', max_length=100)),
                ('p_bank_IFSC_code', models.CharField(default='', max_length=100)),
                ('p_bank_name', models.CharField(default='', max_length=500)),
                ('p_bank_branch', models.CharField(default='', max_length=500)),
                ('p_digital_signature', models.ImageField(blank=True, default='', null=True, upload_to='partner_digital_signature')),
                ('p_business_logo', models.ImageField(blank=True, default='', null=True, upload_to='partner_business_logo')),
                ('p_business_stamp', models.ImageField(blank=True, default='', null=True, upload_to='partner_business_stamp')),
                ('p_business_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='category_and_tags.business_category')),
                ('p_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MerchantProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_business_name', models.CharField(default='', max_length=500)),
                ('m_pin_code', models.CharField(default='', max_length=20)),
                ('m_city', models.CharField(default='', max_length=500)),
                ('m_district', models.CharField(default='', max_length=500)),
                ('m_state', models.CharField(default='', max_length=500)),
                ('m_address', models.CharField(default='', max_length=1000)),
                ('m_landline_number', models.CharField(default='', max_length=20)),
                ('m_alternate_mobile_number', models.CharField(default='', max_length=20)),
                ('m_company_email', models.EmailField(blank=True, default='', max_length=254)),
                ('m_alternate_email', models.EmailField(blank=True, default='', max_length=254)),
                ('m_pan_number', models.CharField(default='', max_length=50)),
                ('m_gstin', models.CharField(default='', max_length=100)),
                ('m_GSTIN_certificate', models.FileField(blank=True, default='', null=True, upload_to='merchant_GSTIN_certificate')),
                ('m_cin', models.CharField(default='', max_length=100)),
                ('m_CIN_certificate', models.FileField(blank=True, default='', null=True, upload_to='merchant_CIN_certificate')),
                ('m_bank_account_number', models.CharField(default='', max_length=100)),
                ('m_bank_IFSC_code', models.CharField(default='', max_length=100)),
                ('m_bank_name', models.CharField(default='', max_length=500)),
                ('m_bank_branch', models.CharField(default='', max_length=500)),
                ('m_digital_signature', models.ImageField(blank=True, default='', null=True, upload_to='merchant_digital_signature')),
                ('m_business_logo', models.ImageField(blank=True, default='', null=True, upload_to='merchant_business_logo')),
                ('m_business_stamp', models.ImageField(blank=True, default='', null=True, upload_to='merchant_business_stamp')),
                ('m_active_account', models.BooleanField(default=False)),
                ('m_business_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='category_and_tags.business_category')),
                ('m_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant_users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
