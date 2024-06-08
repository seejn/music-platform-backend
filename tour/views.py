from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from .models import Tour,CustomUser
from django.db import IntegrityError
from .serializers import TourSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from backend.permission import IsArtist, IsAdmin,IsAdminOrArtist,IsUser,IsAdminOrArtistOrUser,IsUserOrArtist
import json

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

@api_view(['POST'])
@permission_classes([IsAdmin])
def create_tour(request):
    dict_data = request.POST.dict()
    input_fields = list(dict_data.keys())
    
    required_fields=['title','artist','date','time','location']

    if not check_required_fields(input_fields, required_fields):
        return JsonResponse({"message": f"Required Fields: {required_fields}"}, safe=False, status=400)    

    artist_id = dict_data.get('artist')
    artist=None
    
    dict_data.pop('artist')
    try:
        artist =CustomUser.objects.get(pk=artist_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message":"Artist not available"}, status=404)
    
    new_tour = Tour.objects.create(**dict_data,artist=artist)
    new_tour = TourSerializer(new_tour).data

    return JsonResponse({"message": "New Tour Added Successfully", "data": new_tour}, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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

    if not does_field_exist(input_fields,required_fields):
        return JsonResponse({"message": "Field not Available"}, status=400)  
    
    tour.__dict__.update(dict_data)
    try:
        tour.save()
    except IntegrityError:
        return JsonResponse({"message": "Not Available"}, status=404)   

    tour = Tour.objects.get(pk=tour_id)
    updated_tour= TourSerializer(tour).data
    
    return JsonResponse({"message": "Track Updated Successfully", "data": updated_tour}, status=200)

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
