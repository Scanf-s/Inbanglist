from django.contrib import admin
from .models import YoutubeModel
# Register your models here.

@admin.register(YoutubeModel)
class YoutubeAdmin(admin.ModelAdmin):
    pass
