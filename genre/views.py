from django.shortcuts import render
from django.http import JsonResponse
from .serializers import GenreSerializer
from .models import Genre
# Create your views here.
def get_all_genres(request):

    genres = Genre.objects.all()
    genres = GenreSerializer(genres, many=True).data

    return JsonResponse({"message": "Genres", "data": genres}, status=200)