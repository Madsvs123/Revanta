from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.forecasts.models import CapacityAssumption, Outlook, OutlookLine, Scenario
from apps.forecasts.serializers import (
    CapacityAssumptionSerializer,
    OutlookLineSerializer,
    OutlookSerializer,
    ScenarioSerializer,
)
from apps.forecasts.services import build_outlook


class OutlookViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Outlook.objects.prefetch_related("scenarios", "lines", "assumptions")
    serializer_class = OutlookSerializer
    resource_name = "forecasts"

    @action(detail=False, methods=["post"])
    def refresh(self, request):
        outlook = build_outlook(request.organization)
        return Response(OutlookSerializer(outlook).data)


class ScenarioViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Scenario.objects.select_related("outlook")
    serializer_class = ScenarioSerializer
    resource_name = "forecasts"
    filterset_fields = ("outlook",)


class OutlookLineViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = OutlookLine.objects.select_related("outlook")
    serializer_class = OutlookLineSerializer
    resource_name = "forecasts"
    filterset_fields = ("outlook",)


class CapacityAssumptionViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = CapacityAssumption.objects.select_related("outlook")
    serializer_class = CapacityAssumptionSerializer
    resource_name = "forecasts"
