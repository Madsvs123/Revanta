from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.entitlements.views import (
    AccessCheckViewSet,
    EntitlementOverrideViewSet,
    EntitlementViewSet,
    FeatureDefinitionViewSet,
    PlanGrantViewSet,
)

router = DefaultRouter()
router.register("entitlements/features", FeatureDefinitionViewSet, basename="entitlement-features")
router.register("entitlements/grants", PlanGrantViewSet, basename="entitlement-grants")
router.register("entitlements", EntitlementViewSet, basename="entitlements")
router.register("entitlements/overrides", EntitlementOverrideViewSet, basename="entitlement-overrides")
router.register("entitlements/checks", AccessCheckViewSet, basename="entitlement-checks")

urlpatterns = [path("", include(router.urls))]
