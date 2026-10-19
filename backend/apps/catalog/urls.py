from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.catalog.views import (
    AddonViewSet,
    BundleViewSet,
    CouponViewSet,
    PlanViewSet,
    PriceTierViewSet,
    ProductViewSet,
    RegionalPriceViewSet,
)

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("plans", PlanViewSet, basename="plans")
router.register("price-tiers", PriceTierViewSet, basename="price-tiers")
router.register("addons", AddonViewSet, basename="addons")
router.register("bundles", BundleViewSet, basename="bundles")
router.register("coupons", CouponViewSet, basename="coupons")
router.register("regional-prices", RegionalPriceViewSet, basename="regional-prices")

urlpatterns = [path("", include(router.urls))]
