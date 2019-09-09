# Generated by Django 2.2.3 on 2019-09-09 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='message')),
                ('added', models.DateTimeField(auto_now_add=True, verbose_name='added')),
                ('unseen', models.BooleanField(default=True, verbose_name='unseen')),
                ('archived', models.BooleanField(default=False, verbose_name='archived')),
                ('on_site', models.BooleanField(verbose_name='on site')),
                ('target_url', models.URLField(blank=True, null=True, verbose_name='target url')),
            ],
            options={
                'verbose_name': 'notice',
                'verbose_name_plural': 'notices',
                'ordering': ['-added'],
            },
        ),
        migrations.CreateModel(
            name='NoticeQueueBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickled_data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NoticeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=40, verbose_name='label')),
                ('display', models.CharField(max_length=50, verbose_name='display')),
                ('past_tense', models.CharField(max_length=100, verbose_name='Past Tense')),
                ('description', models.CharField(max_length=100, verbose_name='description')),
                ('default', models.IntegerField(verbose_name='default')),
                ('state', models.SmallIntegerField(choices=[(-1, 'Deleted'), (0, 'Draft'), (1, 'Published'), (2, 'Published - Staff only')], default=1, verbose_name='Publish state')),
            ],
            options={
                'verbose_name': 'notice type',
                'verbose_name_plural': 'notice types',
            },
        ),
        migrations.CreateModel(
            name='NoticeLastSeen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.DateTimeField(auto_now=True, verbose_name='seen')),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinax_notifications.Notice')),
                ('recipient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notices_seen', to=settings.AUTH_USER_MODEL, verbose_name='recipient')),
            ],
        ),
        migrations.AddField(
            model_name='notice',
            name='notice_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinax_notifications.NoticeType', verbose_name='notice type'),
        ),
        migrations.AddField(
            model_name='notice',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notices', to=settings.AUTH_USER_MODEL, verbose_name='recipient'),
        ),
        migrations.AddField(
            model_name='notice',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_notices', to=settings.AUTH_USER_MODEL, verbose_name='sender'),
        ),
        migrations.AddField(
            model_name='notice',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notice_site', to='sites.Site', verbose_name='site'),
        ),
        migrations.CreateModel(
            name='NoticeSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medium', models.CharField(choices=[(0, 'email')], max_length=1, verbose_name='medium')),
                ('send', models.BooleanField(default=False, verbose_name='send')),
                ('scoping_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('notice_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinax_notifications.NoticeType', verbose_name='notice type')),
                ('scoping_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'notice setting',
                'verbose_name_plural': 'notice settings',
                'unique_together': {('user', 'notice_type', 'medium', 'scoping_content_type', 'scoping_object_id')},
            },
        ),
    ]
