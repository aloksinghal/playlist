# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track8', '0002_playlistsong_playlisttag'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='url',
            field=models.URLField(default='www.youtube.com'),
            preserve_default=False,
        ),
    ]
