from django.http import JsonResponse
from django.db.models import Count
from Roles.models import Role
from Cusers.models import CustomUser


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



def all_artists_album_favourites(request):
    artist_role = Role.objects.get(pk=2)
    
    artists = artist_role.user.all()
    data = []
    
    for artist in artists:
        albums = artist.album_set.all()
        album_data = []
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
            album_data.append(album_info)
        
        artist_data = {
            'artist': artist.email,
            'albums': album_data,
            "total_favourite_count":total_favourite_count
            

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
