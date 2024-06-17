from django.contrib import admin
from .models import ChzzkModel
# Register your models here.

@admin.register(ChzzkModel)
class ChzzkAdmin(admin.ModelAdmin):
    pass
