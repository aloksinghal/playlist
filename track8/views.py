from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from track8 import models
from track8 import serializers
from track8 import helper
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Q, F


class SongList(APIView):

    def get(self, request, pk, format=None):
        """API to get a single song by id"""
        try:
            song = models.Song.objects.get(id=pk)
        except models.Song.DoesNotExist:
            return Response({"message": "song not found"}, status=status.HTTP_200_OK)
        serialized_songs = serializers.SongSerializer(song)
        return Response({"message": "SUCCESS", 'data' : serialized_songs.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """API to update song details by ID"""
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
        """API to delete song"""
        try:
            song = models.Song.objects.get(id=pk)
        except models.Song.DoesNotExist:
            return Response({"message": "song not found"}, status=status.HTTP_200_OK)
        song.delete()
        models.PlaylistSong.objects.filter(song_id=pk).delete()
        return Response({"message": "SUCCESS"}, status=status.HTTP_200_OK)


class CreateSong(APIView):

    def post(self, request, format=None):
        """API to create a new song"""
        name = request.data.get('name', None)
        url = request.data.get('url', None)

        if not (name and url):
            return Response({"message": "both name and url are required"}, status=status.HTTP_200_OK)
        song = models.Song.objects.create(name=name, url=url)
        serialized_song = serializers.SongSerializer(song)
        return Response({"message": "SUCCESS", 'data' : serialized_song.data}, status=status.HTTP_201_CREATED)


class CreateTag(APIView):

    def post(self, request, format=None):
        """API to create a tag"""
        name = request.data.get('name', None)

        if not name:
            return Response({"message" : "name is required"}, status=status.HTTP_200_OK)
        try:
            tag = models.Tag.objects.create(name=name)
        except IntegrityError:
            tag = models.Tag.objects.get(name=name)
        serialized_tag = serializers.TagSerializer(tag)
        return Response({"message": "SUCCESS", 'data' : serialized_tag.data}, status=status.HTTP_200_OK)


class TagList(APIView):

    def get(self, request, pk, format=None):
        """API to get details of a tag by ID"""
        try:
            tag = models.Tag.objects.get(id=pk)
        except models.Tag.DoesNotExist:
            return Response({"message": "tag not found"}, status=status.HTTP_200_OK)

        serialized_tag = serializers.TagSerializer(tag)
        return Response({"message": "SUCCESS", 'data' : serialized_tag.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        """API to delete tag by ID"""
        try:
            tag = models.Tag.objects.get(id=pk)
        except models.Tag.DoesNotExist:
            return Response({"message": "tag not found"}, status=status.HTTP_200_OK)
        tag.delete()
        models.PlaylistTag.objects.filter(tag_id=pk).delete()
        return Response({"message": "SUCCESS"}, status=status.HTTP_200_OK)

class CreatePlaylist(APIView):

    def post(self, request, format=None):
        """API to create a playlist"""
        name = request.data.get('name', None)
        if not name:
            return Response({"message" : "name is required"}, status=status.HTTP_200_OK)
        try:
            playlist = models.Playlist.objects.create(name=name)
        except IntegrityError:
            return Response({"message" : "playlist with this name already exists"}, status=status.HTTP_200_OK)
        serialized_playlist = serializers.PlaylistSerializer(playlist)
        return Response({"message": "SUCCESS", 'data' : serialized_playlist.data}, status=status.HTTP_201_CREATED)

class PlaylistDetails(APIView):

    def get(self, request, pk, format=None):
        """API to retrieve a single playlist with songs and tags associated to it"""
        try:
            playlist = models.Playlist.objects.get(id=pk)
        except models.Playlist.DoesNotExist:
            return Response({"message" : "playlist not found"}, status=status.HTTP_200_OK)
        playlist_data = helper.get_playlist_data(playlist)
        return Response({"message": "SUCCESS", 'data' : playlist_data}, status=status.HTTP_200_OK)



class Searchtags(APIView):

    def get(self, request, format=None):
        """API to get playlists related to a combination of tags separated by _ """
        tags= request.GET.get('tags',None)
        if not tags:
            return Response({"message: at least one tag is needed"}, status= status.HTTP_200_OK)
        tag_list = tags.split("_")
        tag_ids = models.Tag.objects.filter(name__in=tag_list).values_list("id", flat=True)
        playlists = helper.get_related_playlists(tag_ids)
        serialized_playlists = serializers.PlaylistSerializer(playlists, many=True)
        related_tags = helper.get_related_tags(tag_ids)
        serialized_tags = serializers.TagSerializer(related_tags, many=True)
        return Response({"message": "SUCCESS", 'playlist_data' : serialized_playlists.data,
                         'tag_data': serialized_tags.data}, status=status.HTTP_200_OK)

class AddSong(APIView):

    def put(self, request, pk, format=None):
        """API to add song to a playlist"""
        try:
            playlist = models.Playlist.objects.get(id=pk)
        except models.Playlist.DoesNotExist:
            return Response({"message" : "playlist not found"}, status=status.HTTP_200_OK)
        song_id = request.data.get('song_id', None)
        try:
            song = models.Song.objects.get(id=song_id)
        except models.Song.DoesNotExist:
            return Response({"message" : "song not found"}, status=status.HTTP_200_OK)
        mapping = models.PlaylistSong.objects.get_or_create(song=song, playlist=playlist)

        return Response({"message": "SUCCESS"}, status=status.HTTP_200_OK)

class RemoveSong(APIView):
    """API to remove song from a playlist"""
    def put(self, request, pk, format=None):
        try:
            playlist = models.Playlist.objects.get(id=pk)
        except models.Playlist.DoesNotExist:
            return Response({"message" : "playlist not found"}, status=status.HTTP_200_OK)
        song_id = request.data.get('song_id', None)
        try:
            song = models.Song.objects.get(id=song_id)
        except models.Song.DoesNotExist:
            return Response({"message" : "song not found"}, status=status.HTTP_200_OK)
        try:
            mapping = models.PlaylistSong.objects.get(song=song, playlist=playlist)
            mapping.delete()
        except models.PlaylistSong.DoesNotExist:
            return Response({"message": "no mapping found"}, status=status.HTTP_200_OK)
        return Response({"message": "SUCCESS"}, status=status.HTTP_200_OK)

class AddTag(APIView):

    def put(self, request, pk, format=None):
        """API to add tag to a playlist"""
        try:
            playlist = models.Playlist.objects.get(id=pk)
        except models.Playlist.DoesNotExist:
            return Response({"message" : "playlist not found"}, status=status.HTTP_200_OK)
        tag_name = request.data.get('tag_name', None)
        tag, created = models.Tag.objects.get_or_create(name=tag_name, defaults={})

        mapping = models.PlaylistTag.objects.get_or_create(tag=tag, playlist=playlist)

        return Response({"message": "SUCCESS"}, status=status.HTTP_200_OK)

class RemoveTag(APIView):
    def put(self, request, pk, format=None):
        """API to remove tag from a playlist"""
        try:
            playlist = models.Playlist.objects.get(id=pk)
        except models.Playlist.DoesNotExist:
            return Response({"message" : "playlist not found"}, status=status.HTTP_200_OK)
        tag_id = request.data.get('tag_id', None)
        try:
            tag = models.Tag.objects.get(id=tag_id)
        except models.Tag.DoesNotExist:
            return Response({"message" : "tag not found"}, status=status.HTTP_200_OK)
        try:
            mapping = models.PlaylistTag.objects.get(tag=tag, playlist=playlist)
            mapping.delete()
        except models.PlaylistTag.DoesNotExist:
            return Response({"message" : "mapping not found"}, status=status.HTTP_200_OK)

        return Response({"message": "SUCCESS"}, status=status.HTTP_200_OK)

class IncrementLikeCount(APIView):

    def put(self, request, pk, format=None):
        try:
            playlist = models.Playlist.objects.get(id=pk)
        except models.Playlist.DoesNotExist:
            return Response({"message" : "playlist not found"}, status=status.HTTP_200_OK)
        playlist.like_count = F('like_count') + 1
        playlist.save()
        playlist = models.Playlist.objects.get(id=pk)
        return Response({"message": "SUCCESS", "new_count": playlist.like_count}, status=status.HTTP_200_OK)

class DecrementLikeCount(APIView):

    def put(self, request, pk, format=None):
        try:
            playlist = models.Playlist.objects.get(id=pk)
        except models.Playlist.DoesNotExist:
            return Response({"message" : "playlist not found"}, status=status.HTTP_200_OK)
        playlist.like_count = F('like_count') - 1
        playlist.save()
        playlist = models.Playlist.objects.get(id=pk)
        return Response({"message": "SUCCESS", "new_count": playlist.like_count}, status=status.HTTP_200_OK)



        




























        

