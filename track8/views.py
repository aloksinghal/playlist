from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from track8 import models
from track8 import serializers
from django.db import transaction

class SongList(APIView):

	def get(self, request, pk, format=None):
		song = models.Song.objects.get(id=pk)
		serialized_songs = serializers.SongSerializer(song)
		return Response({"message": "SUCCESS", 'data' : serialized_songs.data}, status=status.HTTP_200_OK)

	def put(self, request, pk, format=None):
		updated_data = request.data.get("updated_data", None)
		if "id" in updated_data:
			return Response({"message": "Can not update id of record"}, status=status.HTTP_200_OK)
		if updated_data:
			song, created = models.Song.objects.update_or_create(id=pk,
    									    defaults=updated_data)
			serialized_song = serializers.SongSerializer(song)
			return Response({"message": "SUCCESS", 'data' : serialized_song.data}, status=status.HTTP_200_OK)
		else:
			return Response({"message": "No data Received"}, status=status.HTTP_200_OK)

	@transaction.atomic
	def delete(self, request, pk, format=None):
		song = models.Song.objects.get(id=pk)
		song.delete()
		models.PlaylistSong.objects.filter(song_id=pk).delete()
		return Response({"message": "SUCCESS"}, status=status.HTTP_200_OK)


class CreateSong(APIView):

	def post(self, request, format=None):
		name = request.data.get('name', None)
		url = request.data.get('url', None)

		if not (name and url):
			return Response({"message": "both name and url are required"}, status=status.HTTP_200_OK)
		song = models.Song.objects.create(name=name, url=url)
		serialized_song = serializers.SongSerializer(song)
		return Response({"message": "SUCCESS", 'data' : serialized_song.data}, status=status.HTTP_201_CREATED)


class CreateTag(APIView):

	def post(self, request, format=None):
		name = request.data.get('name', None)

		if not name:
			return Response({"message" : "name is required"}, status=status.HTTP_200_OK)
		try:
			tag = models.Tag.objects.create(name=name)
		except IntegrityError:
			tag = models.Tag.objects.get(name=Name)
		serialized_tag = serializers.TagSerializer(tag)
		return Response({"message": "SUCCESS", 'data' : serialized_tag.data}, status=status.HTTP_200_OK)


class TagList(APIView):

	def get(self, request, pk, format=None):
		tag = models.Tag.objects.get(id=pk)
		serialized_tag = serializers.TagSerializer(tag)
		return Response({"message": "SUCCESS", 'data' : serialized_tag.data}, status=status.HTTP_200_OK)

	@transaction.atomic
	def delete(self, request, pk, format=None):
		tag = models.Tag.objects.get(id=pk)
		tag.delete()
		models.PlaylistTag.objects.filter(tag_id=pk).delete()
		return Response({"message": "SUCCESS"}, status=status.HTTP_200_OK)

class CreatePlaylist(APIView):

	def post(self, request, format=None):
		name = request.data.get('name', None)
		if not name:
			return Response({"message" : "name is required"}, status=status.HTTP_200_OK)
		playlist = models.Playlist.objects.create(name=name)
		serialized_playlist = serializers.PlaylistSerializer(playlist)
		return Response({"message": "SUCCESS", 'data' : serialized_playlist.data}, status=status.HTTP_201_CREATED)

class PlaylistDetails(APIView):

	def get(self, request, pk, format=None):
		playlist = models.Playlist.objects.get(id=pk)
		serialized_playlist = serializers.PlaylistSerializer(playlist)
		songs_mapping = models.PlaylistSong.objects.filter(playlist=playlist).values_list("song_id", flat=True)
		songs = models.Song.objects.filter(id__in=songs_mapping)
		serialized_songs = serializers.SongSerializer(songs, many=True)
		tags_mapping = models.PlaylistTag.objects.filter(playlist=playlist).values_list("tag_id", flat=True)
		tags = models.Tag.objects.filter(id__in=tags_mapping)
		serialized_tags = serializers.TagSerializer(tags, many = True)
		return_data = {"playlist" : serialized_playlist.data,
						"songs" : serialized_songs.data,
						"tags" : serialized_tags.data}

		return Response({"message": "SUCCESS", 'data' : return_data}, status=status.HTTP_201_CREATED)


















		

