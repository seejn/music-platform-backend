from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied



class IsUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail="Authentication required.")
        
        user_role_id = request.user.role.id
        print(f"User: {request.user}, Role ID: {user_role_id}, Role: {request.user.role}")

        return user_role_id == 1  
    
class IsArtist(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail="Authentication required.")
        
        user_role_id = request.user.role.id  
        print(f"User: {request.user}, Role ID: {user_role_id}, Role: {request.user.role}")

        return user_role_id == 2  


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail="Authentication required.")
        
        user_role_id = request.user.role.id
        print(f"User: {request.user}, Role ID: {user_role_id}, Role: {request.user.role}")

        return user_role_id == 3 

class IsUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail="Authentication required.")
        
        user_role_id = request.user.role.id
        print(f"User: {request.user}, Role ID: {user_role_id}, Role: {request.user.role}")

        return user_role_id == 1 

class IsAdminOrArtist(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied(detail="Authentication required.")
        
        user_role_id = request.user.role.id
        print(f"User: {request.user}, Role ID: {user_role_id}, Role: {request.user.role}")

        return user_role_id in [2, 3]  

