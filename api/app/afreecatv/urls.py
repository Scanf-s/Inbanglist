from django.urls import path
from afreecatv import views

urlpatterns = [
    path('', views.AfreecaTvList.as_view(), name='afreeca_tv_list'),
    path('<int:pk>', views.AfreecaTvDetail.as_view(), name='afreeca_tv_detail'),
]