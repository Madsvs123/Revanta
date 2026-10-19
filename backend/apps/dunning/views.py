from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.dunning.models import DunningCase, DunningPolicy
from apps.dunning.serializers import DunningCaseSerializer, DunningPolicySerializer
from apps.dunning.services import recover_case, run_case_step


class DunningPolicyViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = DunningPolicy.objects.prefetch_related("steps")
    serializer_class = DunningPolicySerializer
    resource_name = "dunning"


class DunningCaseViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = DunningCase.objects.select_related("company", "invoice", "policy").prefetch_related("actions", "reminders")
    serializer_class = DunningCaseSerializer
    resource_name = "dunning"
    filterset_fields = ("status", "company")
    search_fields = ("company__name", "invoice__number")

    @action(detail=True, methods=["post"])
    def advance(self, request, pk=None):
        case = self.get_object()
        recover_case(case)
        case.refresh_from_db()
        return Response(DunningCaseSerializer(case).data)

    @action(detail=True, methods=["post"])
    def recover(self, request, pk=None):
        case = self.get_object()
        recover_case(case)
        return Response(DunningCaseSerializer(case).data)
