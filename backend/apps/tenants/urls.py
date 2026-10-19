from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.tenants.views import (
    BillingEntityViewSet,
    BusinessUnitViewSet,
    CurrencyViewSet,
    OrganizationViewSet,
    SettingsView,
    TaxRegionViewSet,
)

router = DefaultRouter()
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("business-units", BusinessUnitViewSet, basename="business-units")
router.register("billing-entities", BillingEntityViewSet, basename="billing-entities")
router.register("currencies", CurrencyViewSet, basename="currencies")
router.register("tax-regions", TaxRegionViewSet, basename="tax-regions")

urlpatterns = [
    path("prefs/", SettingsView.as_view()),
    path("", include(router.urls)),
]
