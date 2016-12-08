from django.conf.urls import include, patterns, url
from track8 import views

urlpatterns = [
url(r'^song/(?P<pk>[0-9]+)/$', views.SongList.as_view(), name='Song API'),
url(r'^song/$', views.CreateSong.as_view(), name='Song Create API'),
url(r'^tag/$', views.CreateTag.as_view(), name='Tag Create API'),
url(r'^tag/(?P<pk>[0-9]+)/$', views.TagList.as_view(), name='Tag API'),
url(r'^playlist/$', views.CreatePlaylist.as_view(), name='Playlist Create API'),
url(r'^playlist/(?P<pk>[0-9]+)/$', views.PlaylistDetails.as_view(), name='Tag API'),
url(r'^tags/explore/$', views.Searchtags.as_view(), name="Search API"),
url(r'playlist/(?P<pk>[0-9]+)/song/add/$', views.AddSong.as_view(), name="Add Song API"),
url(r'playlist/(?P<pk>[0-9]+)/song/remove/$', views.RemoveSong.as_view(), name="Remove Song API"),
url(r'playlist/(?P<pk>[0-9]+)/tag/add/$', views.AddTag.as_view(), name="Add Tag API"),
url(r'playlist/(?P<pk>[0-9]+)/tag/remove/$', views.RemoveTag.as_view(), name="Remove Tag API"),
url(r'playlist/(?P<pk>[0-9]+)/like_count/increment/$', views.IncrementLikeCount.as_view(), name="Increment Like Count"),
url(r'playlist/(?P<pk>[0-9]+)/like_count/decrement/$', views.DecrementLikeCount.as_view(), name="Decrement Like Count"),

]