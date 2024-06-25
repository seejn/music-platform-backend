from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from .models import Tour,CustomUser
from django.db import IntegrityError
from .serializers import TourSerializer 
from utils.fields import check_required_fields, does_field_exist
from rest_framework.permissions import AllowAny,IsAuthenticated
from backend.permission import IsArtist, IsAdmin,IsAdminOrArtist,IsUser,IsAdminOrArtistOrUser,IsUserOrArtist
import json,datetime
from rest_framework.response import Response
from django.http import HttpRequest
from track.models import Playlist
from album.models import FavouriteAlbum
from track.models import FavouritePlaylist,Music

@api_view(['GET'])
@permission_classes([AllowAny])

def get_all_tours(request):
    all_tours=Tour.objects.all()
    if not all_tours:
        return JsonResponse({"message": "No tour available"}, status=404) 
    serializer = TourSerializer(all_tours, many=True)

    return JsonResponse({"message":f"All Tours","data":serializer.data}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_artist_tour(request,artist_id):
    try:
        artist = CustomUser.objects.get(pk=artist_id)
    
    except CustomUser.DoesNotExist:
        return JsonResponse({"message":"Artist Tour not Available"},status=404)
    
    tours=Tour.objects.all().filter(artist_id=artist_id)

    serializer = TourSerializer(tours,many=True)
    
    return JsonResponse({"message":f"Artist {artist_id} Tours","data":serializer.data}, status=200)


# def format_time_to_12hr(time_str):
#     time_obj = datetime.strptime(time_str, '%H:%M')
#     return time_obj.strftime('%I:%M %p')


@api_view(['POST'])
@permission_classes([IsAdmin,IsAuthenticated])
def create_tour(request):
    dict_data = json.loads(request.body)
    input_fields = list(dict_data.keys())
    print(dict_data)
    
    # required_fields=['title','artist','date','time','location','venue']

    # if not check_required_fields(input_fields, required_fields):
    #     return JsonResponse({"message": f"Required Fields: {required_fields}"}, safe=False, status=400)    

    artist_id = dict_data.get('artist_id')
    artist=None
    
    dict_data.pop('artist_id')
    try:
        artist =CustomUser.objects.get(pk=artist_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message":"Artist not available"}, status=404)
    
    # dict_data['time'] = format_time_to_12hr(dict_data['time'])
    new_tour = Tour.objects.create(**dict_data,artist=artist)
    new_tour = TourSerializer(new_tour).data

    return JsonResponse({"message": "New Tour Added Successfully", "data": new_tour}, status=200)


@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_tour(request,tour_id):
    dict_data=json.loads(request.body)
    input_fields = list(dict_data.keys())

    try:
        tour = Tour.objects.get(pk=tour_id)
    except Tour.DoesNotExist:
        return JsonResponse({"message":"Tour not Available"}, status=404)
    
    required_fields = list(tour.__dict__.keys())

    print(input_fields)
    print(required_fields)

    # if not does_field_exist(input_fields,required_fields):
    #     return JsonResponse({"message": "Field not Available"}, status=400)  
    
    # if 'time' in dict_data:
    #     dict_data['time'] = format_time_to_12hr(dict_data['time'])
        
    tour.__dict__.update(dict_data)
    try:
        tour.save()
    except IntegrityError:
        return JsonResponse({"message": "Not Available"}, status=404)   

    tour = Tour.objects.get(pk=tour_id)
    updated_tour= TourSerializer(tour).data
    
    return JsonResponse({"message": "Tour Updated Successfully", "data": updated_tour}, status=200)

def does_field_exist(input_fields, required_fields):
    return all(field in required_fields for field in input_fields)


@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_tour(request, tour_id):
    try:
        tour = Tour.objects.get(pk=tour_id)
    except Tour.DoesNotExist:
        return JsonResponse({"message": "Tour not Available"}, status=404) 
    
    tour.soft_delete()
    deleted_tour = TourSerializer(tour).data

    return JsonResponse({"message": "Tour Deleted Successfully", "data": deleted_tour}, status=200)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_user_favorite_playlist_tours(request: HttpRequest, user_id):
#     try:
#         favourite_playlist = FavouritePlaylist.objects.filter(user_id=user_id)

#         if not favourite_playlist.exists():
#             random_tour=Tour.objects.order_by("?")
#             random_tour_data=TourSerializer(random_tour,many=True).data
#             return JsonResponse({"data": random_tour_data}, status=200)
        
#         playlist_id=favourite_playlist.objects.filter(playlist_id)
#         tours = Tour.objects.filter(user_id=artist_ids)
#         tours_data = TourSerializer(tours, many=True).data
#         return JsonResponse({"data":tours_data},status=200)

#         tours=Tour.objects.get()
#     except FavouritePlaylist.DoesNotExist:
#         return JsonResponse({"message": "Favourite playlists not found for the user"}, status=404)
#     except Exception as e:
#         return JsonResponse({"message": f"Error in fetching the favourite playlist: {str(e)}"}, status=500)





@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_favorite_playlist_tours(request, user_id):
    try:
      
        favourite_albums = FavouriteAlbum.objects.filter(user_id=user_id)
        favourite_playlists = FavouritePlaylist.objects.filter(user_id=user_id)

        if not favourite_albums.exists() and not favourite_playlists.exists():
           
            random_tours = Tour.objects.order_by("?")
            random_tour_data = TourSerializer(random_tours, many=True).data
            return JsonResponse({"data": random_tour_data}, status=200)
        
    
        artist_ids = []
        if favourite_albums.exists():
            for favourite_album in favourite_albums:
                albums = favourite_album.album.all() 
                for album in albums:
                    tracks = Music.objects.filter(album=album)
                    for track in tracks:
                        artist_ids.append(track.artist_id)
        
        if favourite_playlists.exists():
            for favourite_playlist in favourite_playlists:
                playlists = favourite_playlist.playlist.all()
                for playlist in playlists:
                    tracks = Music.objects.filter(playlist=playlist)
                    for track in tracks:
                        artist_ids.append(track.artist_id)

 
        tours = Tour.objects.filter(artist_id__in=artist_ids).distinct()

        if not tours.exists():
            random_tours = Tour.objects.order_by("?")
            random_tour_data = TourSerializer(random_tours, many=True).data
            return JsonResponse({"data": random_tour_data}, status=200)
     
        tours_data = TourSerializer(tours, many=True).data
        return JsonResponse({"data": tours_data}, status=200)
    
    except FavouriteAlbum.DoesNotExist:
        return JsonResponse({"message": "Favorite albums not found for the user"}, status=404)
    except FavouritePlaylist.DoesNotExist:
        return JsonResponse({"message": "Favourite playlists not found for the user"}, status=404)
    except Exception as e:
        return JsonResponse({"message": f"Error in fetching the favourite playlist: {str(e)}"}, status=500)
    


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_user_favorite_playlist_tours(request: HttpRequest, user_id):
#     try:
#         response = FavouritePlaylist.objects.get(user_id=user_id)
#         tours=Tour.objects.get()
#     except:
#         tours=Tour.objects.order_by("?")
#         tours=TourSerializer(tours,many=True)
#         return JsonResponse({"data": tours.data}, status=200)
#     return JsonResponse({"data": "success"}, status=200)