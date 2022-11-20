# Generated by Django 3.1.4 on 2021-01-29 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OnwerNoticeBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_title', models.CharField(max_length=100)),
                ('notice_file', models.FileField(upload_to='OwnerNoticeDoc/')),
                ('message', models.CharField(max_length=5000)),
                ('o_sent_sms', models.BooleanField(default='0', null=True)),
                ('o_sent_mail', models.BooleanField(default='0', null=True)),
                ('o_notification', models.BooleanField(default='0', null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OwnerSentNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_status', models.CharField(default='0', max_length=5, null=True)),
                ('sent_sms', models.BooleanField(default='0', null=True)),
                ('sent_mail', models.BooleanField(default='0', null=True)),
                ('notification', models.BooleanField(default='0', null=True)),
                ('sent_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('notice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owner_notice_board.onwernoticeboard')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
