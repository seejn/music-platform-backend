
from rest_framework import serializers
from .models import CustomUser, ArtistDetail
from Roles.models import Role
from Roles.serializers import RoleSerializer

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'image', 'role', 'is_deleted']

class ArtistDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistDetail
        fields = ['artist', 'stagename', 'biography', 'dob', 'gender', 'nationality', 'twitter_link', 'facebook_link', 'instagram_link','is_deleted']


  