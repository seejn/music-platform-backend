from django.http import JsonResponse
from django.db.models import Count
from Roles.models import Role
from Cusers.models import CustomUser


def all_artists_song_playlist_counts(request):
    # Get the artist role
    artist_role = Role.objects.get(pk=2)
    
    artists = artist_role.user.all()
    
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


def artist_album_counts(request):
    artist_role = Role.objects.get(pk=2)
    
    artists = artist_role.user.annotate(total_albums=Count('album')).values('email', 'total_albums')
    
    data = list(artists)
    
    return JsonResponse(data, safe=False)

def total_artists(request):
    artist_role = Role.objects.get(pk=2)
    
    total_artists = artist_role.user.count()
    
    data = {
        'total_artists': total_artists
    }
    
    return JsonResponse(data)

def total_users(request):
    total_users = CustomUser.objects.count()
    
    data = {
        'total_users': total_users
    }
    
    return JsonResponse(data)
