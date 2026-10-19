from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.contracts.views import (
    AccountOwnershipViewSet,
    ContractViewSet,
    HealthIndicatorViewSet,
    RenewalViewSet,
    SalesHandoffViewSet,
)

router = DefaultRouter()
router.register("contracts", ContractViewSet, basename="contracts")
router.register("renewals", RenewalViewSet, basename="renewals")
router.register("handoffs", SalesHandoffViewSet, basename="handoffs")
router.register("ownership", AccountOwnershipViewSet, basename="ownership")
router.register("health", HealthIndicatorViewSet, basename="health")

urlpatterns = [path("", include(router.urls))]
