from django.urls import path
from .views import get_all_users,get_user

urlpatterns = [
    path('get_all_users/', get_all_users, name="get_all_users"),
    path('<int:user_id>/', get_user, name="get_user")
]
