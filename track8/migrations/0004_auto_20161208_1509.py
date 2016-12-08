# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track8', '0003_song_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='like_count',
            field=models.IntegerField(default=0, db_index=True),
        ),
    ]
