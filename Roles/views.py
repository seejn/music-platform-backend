from rest_framework import status
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from .models import Role
from .serializers import RoleSerializer
from Cusers.serializers import ArtistSerializer,CustomUserSerializer,ArtistDetailSerializer
from Cusers.models import CustomUser,ArtistDetail
from utils.fields import check_required_fields, does_field_exist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from backend.permission import IsAdmin, IsAdminOrArtist,IsArtist,IsUser,IsUserOrArtist,IsAdminOrArtistOrUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
import json



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Both email and password are required'}, status=status.HTTP_400_BAD_REQUEST)


    try:
        user = CustomUser.objects.get(email=email)
        print(user)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({'error': 'Inactive account'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CustomUserSerializer(user)
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': serializer.data
    }, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_artist(request):
    artist_role = Role.objects.get(pk=2)
    all_artist = artist_role.user.all()
    # all_artist = ArtistDetail.objects.all()
    
    if not all_artist:
        return JsonResponse({"message": "No artists available"}, status=404)

    serializer = ArtistSerializer(all_artist, many=True)
    return JsonResponse({"message": "All Artists", "data": serializer.data}, status=200)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_artist(request, artist_id):
    try:
        artist = CustomUser.objects.get(pk=artist_id)
        
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "Artist not available"}, status=404)

    serializer = ArtistSerializer(artist)
    return JsonResponse({"message": "Artist's Data", "data": serializer.data}, status=200)



@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    dict_data = request.POST.dict()
    input_fields = list(dict_data.keys())
    image = request.FILES.get("image")

    required_fields = ["email", "dob", "gender", "first_name", "last_name", "password"]


    if not check_required_fields(input_fields,required_fields ):
        return JsonResponse({"message": f"Required Fields: {required_fields}"}, safe=False, status=400)  

    password = dict_data.get("password")
    del dict_data["password"]

    user_role=Role.objects.get(pk=1)
    new_user=user_role.user.create(**dict_data,image=image)
    new_user.set_password(password)
    new_user.save()
    
    serializer=CustomUserSerializer(new_user)
    return JsonResponse({"message":"New User Created Successfully.","data":serializer.data},status=200)



@api_view(['POST'])
@permission_classes([AllowAny])
def create_artist(request):
    if request.method == 'POST':

        dict_data = request.POST.dict()
        input_fields = list(dict_data.keys())
        image = request.FILES.get("image")

        print(dict_data)
        print(input_fields)

        required_fields = ["email", "dob", "gender", "first_name", "last_name", "password"]

        if not check_required_fields(input_fields, required_fields):
            return JsonResponse({"message": f"Required Fields: {required_fields}"}, safe=False, status=400)
        
        try:
            """
            biography = dict_data.get('biography')
            Behavior: If the key 'biography' exists in dict_data, its corresponding value is returned and assigned to biography. If the key does not exist, None is returned and assigned to biography.


            biography = dict_data.get('biography', '')
            Behavior: If the key 'biography' exists in dict_data, its corresponding value is returned and assigned to biography. If the key does not exist, an empty string '' is returned and assigned to biography.
            """
            artist_detail = ArtistDetail.objects.create(
                stagename=dict_data.get('stagename'),
                # stagename=dict_data.get('stagename',''),
                biography=dict_data.get('biography'),
                # biography=dict_data.get('biography', ''),
                nationality=dict_data.get('nationality'),
                # nationality=dict_data.get('nationality',''),
                twitter_link=dict_data.get('twitter_link'),
                # twitter_link=dict_data.get('twitter_link', ''),
                facebook_link=dict_data.get('facebook_link'),
                # facebook_link=dict_data.get('facebook_link', ''),
                instagram_link=dict_data.get('instagram_link')
                # instagram_link=dict_data.get('instagram_link', '')
            )
            artist_detail.save()


            artist_role = Role.objects.get(pk=2)  
            dict_data['role'] = artist_role

            new_artist = CustomUser.objects.create(**{key: dict_data[key] for key in ['first_name', 'last_name', 'email', 'dob', 'gender', 'role']},details=artist_detail,image=image)
            
            password = dict_data.get("password")
            new_artist.set_password(password)
            new_artist.save()
            

            serializer = ArtistSerializer(new_artist)
            return JsonResponse({"message": "New Artist Created Successfully.", "data": serializer.data}, status=200)
        except Role.DoesNotExist:
            return JsonResponse({"message": "Artist role does not exist."}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid HTTP method."}, status=405)



@api_view(['PUT'])
@permission_classes([IsUser])
def update_user(request, user_id):
    dict_data = json.loads(request.body)
    input_fields = list(dict_data.keys())

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not Available"}, status=404)

    required_fields = list(user.__dict__.keys())

    if not all(field in required_fields for field in input_fields):
        return JsonResponse({"message": "Field not Available"}, status=404)

    if request.user.id != user.id:
        raise PermissionDenied("You do not have permission to perform this action.")

    for key, value in dict_data.items():
        setattr(user, key, value)
    
    try:
        user.save()
    except IntegrityError:
        return JsonResponse({"message": "Already Exists"}, status=400)

    updated_user = CustomUserSerializer(user).data
    return JsonResponse({"message": "User Updated Successfully", "data": updated_user}, status=200)


@api_view(['PUT'])
@permission_classes([IsArtist])
def update_personal_artist_info(request, artist_id):
    dict_data = json.loads(request.body)
    input_fields = list(dict_data.keys())

    try:
        artist = CustomUser.objects.get(pk=artist_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "Artist not Available"}, status=404)

    required_fields = list(artist.__dict__.keys())

    if not does_field_exist(input_fields, required_fields):
        return JsonResponse({"message": "Field not Available"}, status=404)
        
    if request.user != artist:
        raise PermissionDenied("You do not have permission to perform this action.")

    artist.__dict__.update(dict_data)
    try:
        artist.save()
    except IntegrityError:
        return JsonResponse({"message": "Already Exists"}, status=400)

    updated_artist = CustomUserSerializer(artist).data
    return JsonResponse({"message": "Artist Updated Successfully", "data": updated_artist}, status=200)

from rest_framework.permissions import IsAuthenticated




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# def update_artist_info(request, artist_id):

#     dict_data = json.loads(request.body)
#     input_fields = list(dict_data.keys())

#     try:
#         artist = ArtistDetail.objects.get(artist_id=artist_id)
#     except ArtistDetail.DoesNotExist:
#         return JsonResponse({"message": "Artist not Available"}, status=404)

#     required_fields = list(artist.__dict__.keys())

#     print(input_fields)
#     print(required_fields)
#     if not does_field_exist(input_fields, required_fields):
#         return JsonResponse({"message": "Field not Available"}, status=404)

#     artist.__dict__.update(dict_data)
#     try:
#         artist.save()
#     except IntegrityError:
#         return JsonResponse({"message": "Already Exists"}, status=400)

#     artist = ArtistDetail.objects.get(pk=artist_id)
#     updated_artist = ArtistDetailSerializer(artist).data

#     return JsonResponse({"message": "Artist Updated Successfully", "data": updated_artist}, status=200)



