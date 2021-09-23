# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
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
                ('in_menu', models.BooleanField(default=False)),
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
                ('blog', models.ForeignKey(to='content.Blog', on_delete=models.CASCADE)),
                ('parent', models.ForeignKey(related_name='child', blank=True, to='content.Comment', null=True, on_delete=models.DO_NOTHING)),
            ],
        ),
    ]
