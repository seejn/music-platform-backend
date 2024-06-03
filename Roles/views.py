from rest_framework import status
from rest_framework.exceptions import NotFound
from django.http import JsonResponse
from .models import Role
from .serializers import RoleSerializer
from Cusers.serializers import ArtistSerializer,CustomUserSerializer,ArtistDetailSerializer
from Cusers.models import CustomUser,ArtistDetail
from django.views.decorators.csrf import csrf_exempt
from utils.fields import check_required_fields, does_field_exist
import json
from django.db import IntegrityError

@csrf_exempt
def get_all_artist(request):
    artist_role = Role.objects.get(pk=2)
    all_artist = artist_role.user.all()
    # all_artist = ArtistDetail.objects.all()
    
    if not all_artist:
        return JsonResponse({"message": "No artists available"}, status=404)

    serializer = ArtistSerializer(all_artist, many=True)
    print(serializer.data)
    return JsonResponse({"message": "All Artists", "data": serializer.data}, status=200)


@csrf_exempt
def get_current_artist(request, artist_id):
    try:
        artist_role = Role.objects.get(pk=2)
        all_artist = artist_role.user.all()
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "Artist not available"}, status=404)

    serializer = ArtistSerializer(all_artist)
    return JsonResponse({"message": "Artist's Data", "data": serializer.data}, status=200)

@csrf_exempt
def create_user(request):
    dict_data=json.loads(request.body)
    input_fields = list(dict_data.keys())

    required_fields = ["email", "image", "dob","gender"]

    if not check_required_fields(input_fields,required_fields ):
        return JsonResponse({"message": f"Required Fields: {required_fields}"}, safe=False, status=400)  
    user_role=Role.objects.get(pk=1)

    new_user=user_role.user.create(**dict_data)
    serializer=CustomUserSerializer(new_user)
    return JsonResponse({"message":"New User Created Successfully.","data":serializer.data},status=200)



@csrf_exempt
def create_artist(request):
    if request.method == 'POST':

        dict_data = json.loads(request.body)
        input_fields = list(dict_data.keys())
        required_fields = ["email", "dob", "gender", "stagename", "nationality"]

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

            new_artist = CustomUser.objects.create(**{key: dict_data[key] for key in ['email', 'dob', 'gender', 'role']},details=artist_detail)

            

            serializer = ArtistSerializer(new_artist)
            return JsonResponse({"message": "New Artist Created Successfully.", "data": serializer.data}, status=200)
        except Role.DoesNotExist:
            return JsonResponse({"message": "Artist role does not exist."}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid HTTP method."}, status=405)



@csrf_exempt
def update_user(request, user_id):

    dict_data = json.loads(request.body)
    input_fields = list(dict_data.keys())

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not Available"}, status=404)

    required_fields = list(user.__dict__.keys())


    if not does_field_exist(input_fields, required_fields):
        return JsonResponse({"message": "Field not Available"}, status=404)


    user.__dict__.update(dict_data)
    try:
        user.save()
    except IntegrityError:
        return JsonResponse({"message": "Already Exists"}, status=400)

    user = CustomUser.objects.get(pk=user_id)
    updated_user = CustomUserSerializer(user).data

    return JsonResponse({"message": "User Updated Successfully", "data": updated_user}, status=200)


@csrf_exempt
def update_personal_artist_info(request, artist_id):

    dict_data = json.loads(request.body)
    input_fields = list(dict_data.keys())

    try:
        artist = CustomUser.objects.get(pk=artist_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "Artist not Available"}, status=404)

    required_fields = list(artist.__dict__.keys())

    print(input_fields)
    print(required_fields)

    if not does_field_exist(input_fields, required_fields):
        return JsonResponse({"message": "Field not Available"}, status=404)
    print(artist.__dict__)
    artist.__dict__.update(dict_data)
    try:
        artist.save()
    except IntegrityError:
        return JsonResponse({"message": "Already Exists"}, status=400)

    artist = CustomUser.objects.get(pk=artist_id)
    updated_artist = CustomUserSerializer(artist).data

    return JsonResponse({"message": "Artist Updated Successfully", "data": updated_artist}, status=200)

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

