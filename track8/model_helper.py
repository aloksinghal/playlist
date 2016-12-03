from track8 import models

class PlaylistHelper():

	def add_song_to_playlist(self, song_id, playlist_id):
		models.PlaylistSong.objects.create(song_id=song_id, playlist_id=playlist_id)

	def remove_song_from_playlist(self, song_id, playlist_id):
		playlist_song_mapping = models.PlaylistSong.objects.get(song_id=song_id, playlist_id=playlist_id)
		playlist_song_mapping.delete()
		
	def add_tag_to_playlist(self, tag_id, playlist_id):
		models.PlaylistTag.objects.create(tag_id=tag_id, playlist_id=playlist_id)

	def remove_tag_from_playlist(self, tag_id, playlist_id):
		playlist_tag_mapping = models.PlaylistTag.objects.get(tag_id=tag_id, playlist_id= playlist_id)
		playlist_tag_mapping.delete()
