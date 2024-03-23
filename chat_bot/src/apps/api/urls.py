from django.urls import include, path
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Vink Hackathon",
        default_version='v1',
        description="Schema API for Vink Hackathon",
        # Впиши свою почту, так как ты регал репозиторий
        contact=openapi.Contact(email="i@msavilov.ru"),
        license=openapi.License(name="GNU General Public License v3.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

v1_router = DefaultRouter()


urlpatterns = [
    path('', include(v1_router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
