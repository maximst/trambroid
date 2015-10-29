# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('drupal', '0003_forum_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='child', blank=True, to='drupal.Forum', null=True),
        ),
    ]
