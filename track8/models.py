from django.db import models
from model_utils.models import TimeStampedModel
from redis_helper import RedisHelper

# Create your models here.

class Playlist(TimeStampedModel):
    name = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    play_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Song(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Tag(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        redis_helper_obj = RedisHelper()
        redis_helper_obj.create_tag(self.name)
        super(Tag, self).save(*args, **kwargs)

class PlaylistTag(TimeStampedModel):
    playlist = models.ForeignKey(Playlist)
    tag = models.ForeignKey(Tag)

    def __unicode__(self):
        return self.playlist.name + " " + self.tag.name

class PlaylistSong(TimeStampedModel):
    playlist = models.ForeignKey(Playlist)
    song = models.ForeignKey(Song)


    def __unicode__(self):
        return self.playlist.name + " " + self.song.name



