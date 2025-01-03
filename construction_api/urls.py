from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.views import MaterialViewSet, OrderViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Construction API",
        default_version='v1',
        description="API for construction material management",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('materials/', include('materials.urls')),
    path('schema-viewer/', include('schema_viewer.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

