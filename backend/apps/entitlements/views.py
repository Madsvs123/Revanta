from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.entitlements.models import AccessCheck, Entitlement, EntitlementOverride, FeatureDefinition, PlanGrant
from apps.entitlements.serializers import (
    AccessCheckSerializer,
    EntitlementOverrideSerializer,
    EntitlementSerializer,
    FeatureDefinitionSerializer,
    PlanGrantSerializer,
)
from apps.entitlements.services import check_access, consume, grant_plan_entitlements
from apps.subscriptions.models import Subscription


class FeatureDefinitionViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = FeatureDefinition.objects.all()
    serializer_class = FeatureDefinitionSerializer
    resource_name = "entitlements"
    search_fields = ("name", "code")
    filterset_fields = ("value_type", "is_active")


class PlanGrantViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = PlanGrant.objects.select_related("plan", "feature")
    serializer_class = PlanGrantSerializer
    resource_name = "entitlements"
    filterset_fields = ("plan", "feature")


class EntitlementViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Entitlement.objects.select_related("feature", "company", "subscription")
    serializer_class = EntitlementSerializer
    resource_name = "entitlements"
    filterset_fields = ("company", "subscription", "feature", "enabled")
    search_fields = ("feature__name", "company__name")

    @action(detail=True, methods=["post"])
    def check(self, request, pk=None):
        allowed, detail = check_access(self.get_object(), request.data.get("requested", 1))
        return Response({"allowed": not allowed, "detail": detail})

    @action(detail=True, methods=["post"])
    def consume(self, request, pk=None):
        ok, detail = consume(self.get_object(), request.data.get("quantity", 1))
        return Response({"ok": ok, "detail": detail}, status=200 if ok else 409)

    @action(detail=False, methods=["post"])
    def sync_subscription(self, request):
        subscription = Subscription.objects.get(id=request.data["subscription_id"], organization=request.organization)
        items = grant_plan_entitlements(subscription)
        return Response(EntitlementSerializer(items, many=True).data, status=status.HTTP_201_CREATED)


class EntitlementOverrideViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = EntitlementOverride.objects.select_related("entitlement")
    serializer_class = EntitlementOverrideSerializer
    resource_name = "entitlements"


class AccessCheckViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = AccessCheck.objects.select_related("entitlement")
    serializer_class = AccessCheckSerializer
    resource_name = "entitlements"
    filterset_fields = ("allowed", "entitlement")
