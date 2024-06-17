from django.contrib import admin

from .models import YoutubeModel, YoutubeStreamDetails


class YoutubeStreamDetailsInline(admin.StackedInline):
    model = YoutubeStreamDetails
    extra = 1
    max_num = 1

@admin.register(YoutubeModel)
class YoutubeAdmin(admin.ModelAdmin):
    inlines =  [YoutubeStreamDetailsInline]
