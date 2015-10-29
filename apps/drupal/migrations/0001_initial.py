# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('weight', models.IntegerField(default=0, blank=True)),
                ('language', models.CharField(default=b'ru', max_length=5, choices=[(b'ru', '\u0420\u0443\u0441\u0441\u043a\u0438\u0439'), (b'en', 'English')])),
                ('tid', models.IntegerField(default=0, blank=True)),
                ('url', models.CharField(default=None, max_length=255, null=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('blogs', models.ManyToManyField(to='content.Blog')),
                ('parent', models.ForeignKey(related_name='child', blank=True, to='drupal.Forum', null=True)),
            ],
        ),
    ]
