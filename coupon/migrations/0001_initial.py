# Generated by Django 3.1.6 on 2021-02-08 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CouponModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=50)),
                ('ccode', models.IntegerField()),
                ('vfrom', models.DateField()),
                ('vthrough', models.DateField()),
                ('category', models.CharField(choices=[('', ''), ('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], default='', max_length=50)),
                ('mycustomer', models.BooleanField(default='false')),
                ('greenbill', models.BooleanField(default='false')),
                ('country', models.CharField(choices=[('', ''), ('India', 'India'), ('Afganistan', 'Afganistan'), ('Canada', 'Canada'), ('China', 'China')], default='', max_length=50)),
                ('state', models.CharField(choices=[('', ''), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Goa', 'Goa'), ('Gujrat', 'Gujrat')], default='', max_length=50)),
                ('district', models.CharField(choices=[('', ''), ('Nagpur', 'Nagpur'), ('Bhandra', 'Bhandra'), ('kolhapur', 'kolhapur'), ('Nashik', 'Nashik')], default='', max_length=50)),
                ('gender', models.CharField(choices=[('', ''), ('Male', 'Male'), ('Female', 'Female')], default='', max_length=50)),
                ('agegroup', models.CharField(choices=[('', ''), ('abc', 'abc'), ('xyz', 'xyz'), ('pqr', 'pqr'), ('mno', 'mno')], default='', max_length=50)),
            ],
        ),
    ]
