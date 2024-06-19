from django.contrib import admin

from common.models import CommonModel


# Register your models here.
@admin.register(CommonModel)
class CommonModelAdmin(admin.ModelAdmin):
    pass
