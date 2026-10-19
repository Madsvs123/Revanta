from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.contracts.models import AccountOwnership, Contract, HealthIndicator, RenewalOpportunity, SalesHandoff
from apps.contracts.serializers import (
    AccountOwnershipSerializer,
    ContractSerializer,
    HealthIndicatorSerializer,
    RenewalOpportunitySerializer,
    SalesHandoffSerializer,
)


class ContractViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Contract.objects.select_related("company")
    serializer_class = ContractSerializer
    resource_name = "contracts"
    search_fields = ("name", "number", "company__name")
    filterset_fields = ("status", "company")


class RenewalViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = RenewalOpportunity.objects.select_related("company", "contract")
    serializer_class = RenewalOpportunitySerializer
    resource_name = "payments"
    filterset_fields = ("stage", "company")


class SalesHandoffViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = SalesHandoff.objects.all()
    serializer_class = SalesHandoffSerializer
    resource_name = "contracts"

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        from django.utils import timezone

        handoff = self.get_object()
        handoff.accepted_at = timezone.now()
        handoff.save(update_fields=["accepted_at", "updated_at"])
        if handoff.to_user_id:
            handoff.company.owner = handoff.from_user
            handoff.company.save(update_fields=["owner", "updated_at"])
        return Response(SalesHandoffSerializer(handoff).data)


class AccountOwnershipViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = AccountOwnership.objects.all()
    serializer_class = AccountOwnershipSerializer
    resource_name = "contracts"
    filterset_fields = ("company", "role")


class HealthIndicatorViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = HealthIndicator.objects.select_related("company")
    serializer_class = HealthIndicatorSerializer
    resource_name = "contracts"
    filterset_fields = ("company",)
