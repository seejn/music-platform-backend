from rest_framework import status
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from .models import Role
from .serializers import RoleSerializer
from Cusers.serializers import ArtistSerializer
from Cusers.models import CustomUser



def get_all_artist(request):
        artist_role = Role.objects.get(pk=2)
        all_artist = artist_role.user.all()
        serializer = ArtistSerializer(all_artist, many=True)
        return JsonResponse(serializer.data, safe=False)



def get_current_artist(request, pk):
        try:
            artist = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="Artist not found")

        serializer = RoleSerializer(artist)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

