from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.integrations.models import Connector, Delivery, Endpoint, SyncJob
from apps.integrations.serializers import ConnectorSerializer, DeliverySerializer, EndpointSerializer, SyncJobSerializer
from apps.integrations.services import emit_event, retry_delivery, run_sync


class ConnectorViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Connector.objects.prefetch_related("endpoints")
    serializer_class = ConnectorSerializer
    resource_name = "integrations"
    search_fields = ("name", "provider")
    filterset_fields = ("provider", "status")

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        job = run_sync(self.get_object(), request.data.get("job_type", "customers"))
        return Response(SyncJobSerializer(job).data, status=status.HTTP_201_CREATED)


class EndpointViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Endpoint.objects.select_related("connector")
    serializer_class = EndpointSerializer
    resource_name = "integrations"
    filterset_fields = ("connector", "is_active")


class DeliveryViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Delivery.objects.select_related("endpoint")
    serializer_class = DeliverySerializer
    resource_name = "integrations"
    filterset_fields = ("status", "event_type")

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        return Response(DeliverySerializer(retry_delivery(self.get_object())).data)

    @action(detail=False, methods=["post"])
    def emit(self, request):
        items = emit_event(request.organization, request.data.get("event_type", "manual.test"), request.data.get("payload") or {})
        return Response(DeliverySerializer(items, many=True).data, status=status.HTTP_201_CREATED)


class SyncJobViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = SyncJob.objects.select_related("connector")
    serializer_class = SyncJobSerializer
    resource_name = "integrations"
