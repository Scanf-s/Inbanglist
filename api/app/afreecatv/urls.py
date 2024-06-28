from django.urls import path

from afreecatv.views import AfreecaTvListAPI, AfreecaTvRetrieveUpdateDestroyAPI

urlpatterns = [
    path("", AfreecaTvListAPI.as_view(), name="afreecatv_list"),
    path("<int:pk>/", AfreecaTvRetrieveUpdateDestroyAPI.as_view(), name="afreecatv_retrieve_update_destroy"),
]
