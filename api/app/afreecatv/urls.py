from django.urls import path

from afreecatv.views import AfreecaTvListCreateAPI, AfreecaTvRetrieveUpdateDestroyAPI

urlpatterns = [
    path("", AfreecaTvListCreateAPI.as_view(), name="afreecatv_list_create"),
    path("<int:pk>/", AfreecaTvRetrieveUpdateDestroyAPI.as_view(), name="afreecatv_retrieve_update_destroy"),
]
