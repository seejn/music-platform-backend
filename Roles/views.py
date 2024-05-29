from django.http import JsonResponse
from Cusers.models import Role
from .serializers import UserSerializer

def get_all_artist(request):
    artist_role = Role.objects.get(pk=2)
    all_artist = artist_role.user.all()
    serializer = UserSerializer(all_artist, many=True)
    return JsonResponse(serializer.data, safe=False)


