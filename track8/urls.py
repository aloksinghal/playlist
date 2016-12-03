from django.conf.urls import include, patterns, url
from track8 import views

urlpatterns = [
url(r'^song/(?P<pk>[0-9]+)/$', views.SongList.as_view(), name='Song API'),
url(r'^song/$', views.CreateSong.as_view(), name='Song Create API'),
url(r'^tag/$', views.CreateTag.as_view(), name='Tag Create API'),
url(r'^tag/(?P<pk>[0-9]+)/$', views.TagList.as_view(), name='Tag API'),
url(r'^playlist/$', views.CreatePlaylist.as_view(), name='Playlist Create API'),
url(r'^playlist/(?P<pk>[0-9]+)/$', views.PlaylistDetails.as_view(), name='Tag API'),
]