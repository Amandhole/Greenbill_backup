# Generated by Django 3.1.6 on 2021-02-08 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0004_auto_20210208_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponmodel',
            name='agegroup',
            field=models.CharField(choices=[('', ''), ('abc', 'abc'), ('xyz', 'xyz'), ('pqr', 'pqr'), ('mno', 'mno')], default='Select Age Group', max_length=50),
        ),
        migrations.AlterField(
            model_name='couponmodel',
            name='category',
            field=models.CharField(choices=[('', ''), ('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], default='Select Category', max_length=50),
        ),
        migrations.AlterField(
            model_name='couponmodel',
            name='country',
            field=models.CharField(choices=[('', ''), ('India', 'India'), ('Afganistan', 'Afganistan'), ('Canada', 'Canada'), ('China', 'China')], default='Select country', max_length=50),
        ),
        migrations.AlterField(
            model_name='couponmodel',
            name='district',
            field=models.CharField(choices=[('', ''), ('Nagpur', 'Nagpur'), ('Bhandra', 'Bhandra'), ('kolhapur', 'kolhapur'), ('Nashik', 'Nashik')], default='Select District', max_length=50),
        ),
        migrations.AlterField(
            model_name='couponmodel',
            name='gender',
            field=models.CharField(choices=[('', ''), ('Male', 'Male'), ('Female', 'Female')], default='Select Gender', max_length=50),
        ),
        migrations.AlterField(
            model_name='couponmodel',
            name='state',
            field=models.CharField(choices=[('', ''), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Goa', 'Goa'), ('Gujrat', 'Gujrat')], default='Select State', max_length=50),
        ),
    ]