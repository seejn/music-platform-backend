from django.http import JsonResponse
from django.db.models import Count
from Roles.models import Role
from Cusers.models import CustomUser
from track.models import Music


def all_artists_song_playlist_counts(request):
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

def get_artist_album_favourite_stats(request, artist_id):
    artist = CustomUser.objects.get(pk=artist_id)

    albums_data = []
    albums = artist.album_set.all()

    for album in albums:
        favourites = album.favourite_by.values('user__gender').annotate(count=Count('user__gender')).order_by('user__gender')
        album_info = {
            'id': album.id,
            'title': album.title,
            'favourite_count': album.favourite_by.count(),
            'favourites_by_gender': list(favourites)
        }
        albums_data.append(album_info)

    return JsonResponse({"message": "Artist Album Stats Data", "data": albums_data}, status=200)

def all_artists_album_favorites(request):
    artist_role = Role.objects.get(pk=2)
    
    artists = artist_role.user.all()
    data = []
    
    for artist in artists:
        albums = artist.album_set.all()
        albums_data = []
        total_favourite_count=0
        
        for album in albums:
            total_favourite_count+=album.favourite_by.count()
            favourites = album.favourite_by.values('user__gender').annotate(count=Count('user__gender')).order_by('user__gender')

            album_info = {
                'id': album.id,
                'title': album.title,
                'favourite_count': album.favourite_by.count(),
                'favourites_by_gender': list(favourites)
            }
            albums_data.append(album_info)
        
        artist_data = {
            'artist_id': artist.id,
            'artist': artist.email,
            'albums': albums_data,
            "total_favourite_count":total_favourite_count
        }
        data.append(artist_data)
    
    return JsonResponse(data, safe=False)



def artist_album_counts(request):
    artist_role = Role.objects.get(pk=2)
    
    artists = artist_role.user.annotate(total_albums=Count('album')).values('email', 'total_albums')
    
    data = list(artists)
    
    return JsonResponse(data, safe=False)

def artist_album(request,artist_id):
    artist_role = Role.objects.get(pk=2)
    
    artist = artist_role.user.filter(pk=artist_id).annotate(total_albums=Count('album')).values('total_albums').first()
    if not artist:
        return JsonResponse({'error': 'Artist not found'}, status=404)
    
    return JsonResponse(artist, safe=False)

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

def total_tracks(request):
    total_tracks = Music.objects.all().count()
    
    data = {
        'total_tracks': total_tracks
    }
    
    return JsonResponse(data)

def artist_total_tracks(request,artist_id):
    artist_total_tracks = Music.objects.filter(artist=artist_id).count()
    
    data = {
        'total_tracks': artist_total_tracks
    }
    
    return JsonResponse(data)

