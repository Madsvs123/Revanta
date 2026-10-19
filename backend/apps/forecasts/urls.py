from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.forecasts.views import CapacityAssumptionViewSet, OutlookLineViewSet, OutlookViewSet, ScenarioViewSet

router = DefaultRouter()
router.register("forecasts", OutlookViewSet, basename="forecasts")
router.register("forecast-scenarios", ScenarioViewSet, basename="forecast-scenarios")
router.register("forecast-lines", OutlookLineViewSet, basename="forecast-lines")
router.register("forecast-assumptions", CapacityAssumptionViewSet, basename="forecast-assumptions")

urlpatterns = [path("", include(router.urls))]
