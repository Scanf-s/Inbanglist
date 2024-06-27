from django.urls import path

from chzzk.views import ChzzkListAPI, ChzzkRetrieveUpdateDestroyAPI

urlpatterns = [
    path("", ChzzkListAPI.as_view(), name="chzzk_list_create"),
    path("<int:pk>", ChzzkRetrieveUpdateDestroyAPI.as_view(), name="chzzk_retrieve_update_destroy"),
]
