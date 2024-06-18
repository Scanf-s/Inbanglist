from django.urls import path
from chzzk import views

urlpatterns = [
    path('', views.ChzzkList.as_view(), name='chzzk_list'),
    path('<int:pk>', views.ChzzkDetail.as_view(), name='chzzk_detail'),
]