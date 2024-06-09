from django.urls import path
from . import views

urlpatterns = [
    path('report_track/<int:track_id>/', views.report_track, name="report_track"),
]