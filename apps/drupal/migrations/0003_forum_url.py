# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drupal', '0002_forum_tid'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='url',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
