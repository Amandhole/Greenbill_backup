# Generated by Django 3.1.5 on 2021-03-02 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supports_faq', '0004_blogs_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs_model',
            name='blog_title',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
    ]
