# Generated by Django 3.1.4 on 2021-03-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supports_faq', '0005_blogs_model_blog_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='video_model',
            name='video_title',
            field=models.CharField(default='', max_length=500, null=True),
        ),
    ]
