from rest_framework import status, viewsets
from rest_framework.decorators import action, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from apps.common.mixins import TenantQuerysetMixin
from apps.customers.models import Company
from apps.subscriptions.models import Subscription
from apps.usage.models import AggregationRule, UsageEvent, UsageMetric, UsagePeriod, UsageThreshold
from apps.usage.serializers import (
    AggregationRuleSerializer,
    UsageEventSerializer,
    UsageMetricSerializer,
    UsagePeriodSerializer,
    UsageThresholdSerializer,
)
from apps.usage.services import ingest_event


class UsageIngestThrottle(UserRateThrottle):
    scope = "usage_ingest"


class UsageMetricViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = UsageMetric.objects.all()
    serializer_class = UsageMetricSerializer
    resource_name = "usage"
    search_fields = ("name", "code")


class AggregationRuleViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = AggregationRule.objects.all()
    serializer_class = AggregationRuleSerializer
    resource_name = "usage"
    filterset_fields = ("metric",)


class UsageEventViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = UsageEvent.objects.select_related("metric", "company")
    serializer_class = UsageEventSerializer
    resource_name = "usage"
    http_method_names = ["get", "head", "options"]
    filterset_fields = ("metric", "company", "subscription")
    search_fields = ("idempotency_key",)

    @throttle_classes([UsageIngestThrottle])
    def create(self, request, *args, **kwargs):
        metric = UsageMetric.objects.get(id=request.data["metric"])
        company = Company.objects.get(id=request.data["company"], organization=request.organization)
        subscription = None
        if request.data.get("subscription"):
            subscription = Subscription.objects.get(id=request.data["subscription"], organization=request.organization)
        event, created = ingest_event(
            organization=request.organization,
            metric=metric,
            company=company,
            subscription=subscription,
            payload=request.data,
        )
        return Response(UsageEventSerializer(event).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def bulk(self, request):
        created = 0
        reused = 0
        results = []
        for item in request.data.get("events", []):
            metric = UsageMetric.objects.get(id=item["metric"], organization=request.organization)
            company = Company.objects.get(id=item["company"], organization=request.organization)
            event, is_new = ingest_event(organization=request.organization, metric=metric, company=company, payload=item)
            created += int(is_new)
            reused += int(not is_new)
            results.append(str(event.id))
        return Response({"created": created, "deduplicated": reused, "ids": results})


class UsagePeriodViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = UsagePeriod.objects.select_related("metric", "company")
    serializer_class = UsagePeriodSerializer
    resource_name = "usage"
    filterset_fields = ("metric", "company", "is_closed")


class UsageThresholdViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = UsageThreshold.objects.all()
    serializer_class = UsageThresholdSerializer
    resource_name = "usage"
