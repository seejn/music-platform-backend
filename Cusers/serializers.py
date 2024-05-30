
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
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    detail = ArtistDetailSerializer(source="artistdetail", read_only=True)
    role = RoleSerializer(read_only=True)
    class Meta:
        model = CustomUser
        exclude = [
            'password',
            'is_superuser',
            'is_staff',
            'groups', 
            'user_permissions'
        ]