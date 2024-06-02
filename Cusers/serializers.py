
from rest_framework import serializers
from .models import CustomUser, ArtistDetail
from Roles.models import Role
from Roles.serializers import RoleSerializer

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'image', 'role', 'is_deleted']

class CustomUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'image', 'role', 'is_deleted']

class ArtistDetailSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    class Meta:
        model = ArtistDetail
        fields = '__all__'

