# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('slug', models.SlugField(unique=True, max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('front_page', models.BooleanField(default=True)),
                ('on_top', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('edit_time', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('drupal_nid', models.IntegerField(default=0, max_length=10, blank=True)),
                ('drupal_slug', models.CharField(default=b'', max_length=255, blank=True)),
                ('drupal_type', models.CharField(default=b'blog', max_length=10, blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('preview', models.TextField(default=b'', blank=True)),
                ('body', models.TextField(default=b'')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='content.Blog', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'content_blog_translation',
                'db_tablespace': '',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=64, blank=True)),
                ('body', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('edit_time', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('is_active', models.BooleanField(default=True)),
                ('language', models.CharField(default=b'ru', max_length=5, choices=[(b'ru', '\u0420\u0443\u0441\u0441\u043a\u0438\u0439'), (b'en', 'English')])),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('blog', models.ForeignKey(to='content.Blog')),
                ('parent', models.ForeignKey(related_name='child', blank=True, to='content.Comment', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='blogtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
