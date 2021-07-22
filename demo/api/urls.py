from .views import *

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
schema_view = get_schema_view(
    openapi.Info(
        title = "SmartHome API",
        default_version='v1',
        description="SmartHome API"
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
    authentication_classes=[]
)

router = DefaultRouter()
router.register('home',HomeAPI,basename='homeupdate')
router.register('esp',EspAPI,basename='esp')
router.register('device',DeviceAPI, basename='deviceupdate')
urlpatterns = [
    path('',schema_view.with_ui('swagger', cache_timeout=0), name = 'schema-swagger-ui'),
    path('',include(router.urls)),
    path('login/', views.LoginAPI.as_view(), name = 'login')
]