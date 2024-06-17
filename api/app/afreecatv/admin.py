from django.contrib import admin
from .models import AfreecaTvModel
# Register your models here.

@admin.register(AfreecaTvModel)
class AfreecaTvAdmin(admin.ModelAdmin):
    pass
