from track8 import models
from track8 import serializers

def get_related_tags(tag_ids):
	original_tags = set(tag_ids)
	playlists = models.PlaylistTag.objects.filter(tag_id__in=tag_ids).values_list('playlist_id', flat=True)
	playlist_ids = list(set(playlists))
	tags = models.PlaylistTag.objects.filter(playlist_id__in=playlist_ids).values_list('tag_id', flat=True)
	related_tag_ids = list(set(tags) - original_tags)
	tags = models.Tag.objects.filter(id__in=related_tag_ids)
	return tags

def get_playlist_data(playlist):
	serialized_playlist = serializers.PlaylistSerializer(playlist)
	songs_mapping = models.PlaylistSong.objects.filter(playlist=playlist).values_list("song_id", flat=True)
	songs = models.Song.objects.filter(id__in=songs_mapping)
	serialized_songs = serializers.SongSerializer(songs, many=True)
	tags_mapping = models.PlaylistTag.objects.filter(playlist=playlist).values_list("tag_id", flat=True)
	tags = models.Tag.objects.filter(id__in=tags_mapping)
	serialized_tags = serializers.TagSerializer(tags, many = True)
	playlist_data = {"playlist" : serialized_playlist.data,
					"songs" : serialized_songs.data,
					"tags" : serialized_tags.data}
	return playlist_data

def get_related_playlists(tag_ids):
	playlist_ids = models.PlaylistTag.objects.filter(tag__id__in=tag_ids).values_list("playlist_id", flat=True)
	playlists = models.Playlist.objects.filter(id__in=playlist_ids).order_by('-like_count')
	return playlists