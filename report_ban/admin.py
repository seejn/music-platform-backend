from django.contrib import admin
from .models import RandBTrack, ReportTrack, BannedTrack
# Register your models here.

admin.site.register(RandBTrack)
admin.site.register(ReportTrack)
admin.site.register(BannedTrack)