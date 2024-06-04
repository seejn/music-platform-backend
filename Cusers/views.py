from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from backend.permission import IsAdmin,IsAdminOrArtist,IsArtist,IsUser
import json


@api_view(['GET'])
@permission_classes([IsAdmin])
def get_all_users(request):
    all_users = CustomUser.objects.all()
    serializer = CustomUserSerializer(all_users, many=True)

    return JsonResponse({"message": f"All Users", "data": serializer.data}, status=200) 



@api_view(['GET'])
@permission_classes([IsAdmin])
def get_user(request, user_id):
    user= CustomUser.objects.get(pk=user_id)
    serializer = CustomUserSerializer(user)

    return JsonResponse({"message": f"User {user_id}", "data": serializer.data}, status=200) 




