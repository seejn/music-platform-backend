
from rest_framework import serializers
from .models import CustomUser, ArtistDetail
from Roles.models import Role
from Roles.serializers import RoleSerializer


class ArtistDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistDetail
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    details = ArtistDetailSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name' ,'email', 'image', 'date_joined','role', 'is_deleted', 'details']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name' ,'email', 'image', 'date_joined','role', 'is_deleted', 'details']
