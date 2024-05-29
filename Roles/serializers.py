 
from rest_framework import serializers
from Cusers.models import CustomUser

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['is_staff', 'is_superuser','password','user_permissions','groups']

