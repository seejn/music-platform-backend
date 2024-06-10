from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from Cusers.models import CustomUser
from track.models import Music, Playlist
from album.models import Album
from .serializers import UserStatsSerializer, ArtistStatsSerializer, TrackStatsSerializer, AlbumStatsSerializer, PlaylistStatsSerializer

@api_view(['GET'])
def user_stats_view(request):
    users = CustomUser.objects.all()
    serializer = UserStatsSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def artist_stats_view(request):
    artists = CustomUser.objects.filter(details__isnull=False)
    serializer = ArtistStatsSerializer(artists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def favorite_album_stats_view(request):
    albums = Album.objects.annotate(fav_count=Count('favourite_by')).order_by('-fav_count')
    serializer = AlbumStatsSerializer(albums, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def favorite_playlist_stats_view(request):
    playlists = Playlist.objects.annotate(fav_count=Count('favourite_by')).order_by('-fav_count')
    serializer = PlaylistStatsSerializer(playlists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def track_report_stats_view(request):
    gender = request.query_params.get('gender', None)
    age = request.query_params.get('age', None)

    tracks = Music.objects.all()

    if gender:
        tracks = tracks.filter(artist__gender=gender)
    
    if age:
        age_filter_date = timezone.now().date() - timedelta(years=int(age))
        tracks = tracks.filter(artist__dob__lte=age_filter_date)

    serializer = TrackStatsSerializer(tracks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
