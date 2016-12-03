from rest_framework import serializers
from track8 import models

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = ('id', 'name', 'url')

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Tag
		fields = ('id', 'name')

class PlaylistSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Playlist
		fields = ('id', 'name', 'like_count', 'play_count')
