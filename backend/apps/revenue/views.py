from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.mixins import TenantQuerysetMixin
from apps.forecasts.serializers import OutlookSerializer
from apps.revenue.models import RevenueSnapshot
from apps.revenue.serializers import CohortMetricSerializer, RevenueSnapshotSerializer
from apps.revenue.services import dashboard_payload


class AnalyticsOverviewView(APIView):
    resource_name = "analytics"

    def get(self, request):
        snapshot, history, cohorts, forecast = dashboard_payload(None)
        return Response(
            {
                "snapshot": RevenueSnapshotSerializer(snapshot).data,
                "history": RevenueSnapshotSerializer(history, many=True).data,
                "cohorts": CohortMetricSerializer(cohorts, many=True).data,
                "forecast": OutlookSerializer(forecast).data,
            }
        )


class SnapshotViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = RevenueSnapshot.objects.all()
    serializer_class = RevenueSnapshotSerializer
    resource_name = "analytics"
