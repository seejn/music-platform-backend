 
from rest_framework import serializers
from .models import Role

class RoleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    role = serializers.CharField()