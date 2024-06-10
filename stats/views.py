from django.http import JsonResponse
from django.db.models import Count
from Roles.models import Role
from Cusers.models import CustomUser


def all_artists_song_playlist_counts(request):
    # Get the artist role
    artist_role = Role.objects.get(pk=2)
    
    artists = artist_role.user.all()
    
    # Prepare the data
    data = []
    
    for artist in artists:
        songs = artist.music_set.annotate(playlist_count=Count('playlist')).values('id', 'title', 'playlist_count')
        artist_data = {
            'artist': artist.email,
            'songs': list(songs)
        }
        data.append(artist_data)
    
    return JsonResponse(data, safe=False)


def all_artists_album_favorites(request):
    artist_role = Role.objects.get(pk=2)
    
    artists = artist_role.user.all()
    data = []
    
    for artist in artists:
        albums = artist.album_set.annotate(favorite_count=Count('favourite_by')).values('id', 'title', 'favorite_count')
        artist_data = {
            'artist': artist.email,
            'albums': list(albums)
        }
        data.append(artist_data)
    
    return JsonResponse(data, safe=False)
