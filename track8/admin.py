from django.contrib import admin
from track8 import models
# Register your models here.

@admin.register(models.Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    pass

@admin.register(models.PlaylistTag)
class PlaylistTagAdmin(admin.ModelAdmin):
    pass
