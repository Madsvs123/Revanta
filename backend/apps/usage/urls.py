from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.usage.views import (
    AggregationRuleViewSet,
    UsageEventViewSet,
    UsageMetricViewSet,
    UsagePeriodViewSet,
    UsageThresholdViewSet,
)

router = DefaultRouter()
router.register("usage/metrics", UsageMetricViewSet, basename="usage-metrics")
router.register("usage/rules", AggregationRuleViewSet, basename="usage-rules")
router.register("usage/events", UsageEventViewSet, basename="usage-events"
router.register("usage/periods", UsagePeriodViewSet, basename="usage-periods")
router.register("usage/thresholds", UsageThresholdViewSet, basename="usage-thresholds")

urlpatterns = [path("", include(router.urls))]
