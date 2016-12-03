# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('track8', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('playlist', models.ForeignKey(to='track8.Playlist')),
                ('song', models.ForeignKey(to='track8.Song')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlaylistTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('playlist', models.ForeignKey(to='track8.Playlist')),
                ('tag', models.ForeignKey(to='track8.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
