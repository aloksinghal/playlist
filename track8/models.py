from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.

class Playlist(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    like_count = models.IntegerField(default=0, db_index=True)
    play_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Song(TimeStampedModel):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __unicode__(self):
        return self.name

class Tag(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

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



