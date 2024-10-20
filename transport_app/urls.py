from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RouteViewSet, StationViewSet, TripViewSet, DriverViewSet, VehicleViewSet, SubscriptionViewSet, UserViewSet, RouteStationViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'stations', StationViewSet)
router.register(r'trips', TripViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'routesstations', RouteStationViewSet)

router.register(r'users', UserViewSet)

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="PT API",
        default_version='v1',
        description="API for managing public transportation data (routes, stations, trips, drivers, etc.)",
        contact=openapi.Contact(email="contact@yourdomain.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]