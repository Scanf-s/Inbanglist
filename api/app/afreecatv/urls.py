
from django.urls import path, include
from afreecatv import views

urlpatterns = [
    path('', views.AfreecaTvListAPI.as_view({'get': 'list'}), name='afreecatv_list'),
    path('<int:pk>', views.AfreecaTvListAPI.as_view({'get': 'retrieve'}), name='afreecatv_detail'),
]