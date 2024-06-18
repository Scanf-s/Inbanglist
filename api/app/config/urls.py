from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

admin_urls = [
    path('admin/', admin.site.urls),
]

api_urls = [
    path('api/v1/afreecatv/', include('afreecatv.urls')),
    path('api/v1/chzzk/', include('chzzk.urls')),
    path('api/v1/youtube/', include('youtube.urls')),
]

drf_spectacular_urls = [
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

rest_framework_simplejwt_urls = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = admin_urls + api_urls + drf_spectacular_urls + rest_framework_simplejwt_urls

# 추후, 프론트 제공 시 제거할 코드임!!!
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

