from rest_framework import viewsets

from apps.catalog.models import Addon, Bundle, Coupon, Plan, PriceTier, Product, RegionalPrice
from apps.catalog.serializers import (
    AddonSerializer,
    BundleSerializer,
    CouponSerializer,
    PlanSerializer,
    PriceTierSerializer,
    ProductSerializer,
    RegionalPriceSerializer,
)
from apps.common.mixins import ArchiveMixin, TenantQuerysetMixin


class ProductViewSet(TenantQuerysetMixin, ArchiveMixin, viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("plans__tiers", "plans__regional_prices")
    serializer_class = ProductSerializer
    resource_name = "invoices"
    search_fields = ("name", "sku")
    filterset_fields = ("is_active", "product_type")


class PlanViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Plan.objects.prefetch_related("tiers", "regional_prices")
    serializer_class = PlanSerializer
    resource_name = "plans"
    search_fields = ("name", "code")
    filterset_fields = ("product", "interval", "is_active", "billing_model")


class PriceTierViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = PriceTier.objects.all()
    serializer_class = PriceTierSerializer
    resource_name = "plans"
    filterset_fields = ("plan", "currency")


class AddonViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Addon.objects.all()
    serializer_class = AddonSerializer
    resource_name = "addons"
    search_fields = ("name", "code")


class BundleViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Bundle.objects.prefetch_related("plans", "addons")
    serializer_class = BundleSerializer
    resource_name = "bundles"


class CouponViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    resource_name = "coupons"
    search_fields = ("name", "code")
    filterset_fields = ("is_active", "duration")


class RegionalPriceViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = RegionalPrice.objects.all()
    serializer_class = RegionalPriceSerializer
    resource_name = "plans"
    filterset_fields = ("plan", "country")
