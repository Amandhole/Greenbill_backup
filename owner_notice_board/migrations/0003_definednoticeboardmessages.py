# Generated by Django 3.1.4 on 2021-09-28 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner_notice_board', '0002_onwernoticeboard_receiver_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefinedNoticeBoardMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=5000)),
            ],
        ),
    ]