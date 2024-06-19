from django.urls import path

from chzzk import views

urlpatterns = [
    path("", views.ChzzkListAPI.as_view({"get": "list"}), name="chzzk_list"),
    path("<int:pk>", views.ChzzkListAPI.as_view({"get": "retrieve"}), name="chzzk_detail"),
]
