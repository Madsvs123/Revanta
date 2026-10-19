from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.integrations.views import ConnectorViewSet, DeliveryViewSet, EndpointViewSet, SyncJobViewSet

router = DefaultRouter()
router.register("integrations/connectors", ConnectorViewSet, basename="connectors")
router.register("integrations/endpoints", EndpointViewSet, basename="endpoints")
router.register("integrations/deliveries", DeliveryViewSet, basename="deliveries")
router.register("integrations/jobs", SyncJobViewSet, basename="sync-jobs")

urlpatterns = [path("", include(router.urls)]
