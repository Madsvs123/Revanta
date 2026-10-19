from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.commissions.models import Accrual, CommissionPlan, CommissionTier, Payout
from apps.commissions.serializers import AccrualSerializer, CommissionPlanSerializer, CommissionTierSerializer, PayoutSerializer
from apps.accounts.models import User
from apps.commissions.services import accrue, build_payout, mark_paid
from apps.customers.models import Company


class CommissionPlanViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = CommissionPlan.objects.prefetch_related("tiers")
    serializer_class = CommissionPlanSerializer
    resource_name = "commissions"


class CommissionTierViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = CommissionTier.objects.select_related("plan")
    serializer_class = CommissionTierSerializer
    resource_name = "commissions"
    filterset_fields = ("plan",)


class AccrualViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Accrual.objects.select_related("owner", "company", "plan")
    serializer_class = AccrualSerializer
    resource_name = "commissions"
    filterset_fields = ("owner", "status", "period", "source")

    def create(self, request, *args, **kwargs):
        company = Company.objects.get(id=request.data["company"], organization=request.organization)
        owner = User.objects.filter(id=request.data.get("owner")).first() or request.user
        record = accrue(
            organization=request.organization,
            owner=owner,
            company=company,
            basis_amount=request.data.get("basis_amount") or request.data.get("amount", 0),
            source=request.data.get("source", "new_logo"),
            period=request.data.get("period"),
        )
        return Response(AccrualSerializer(record).data, status=status.HTTP_201_CREATED)


class PayoutViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Payout.objects.select_related("owner")
    serializer_class = PayoutSerializer
    resource_name = "commissions"
    filterset_fields = ("owner", "status", "period")

    @action(detail=False, methods=["post"])
    def generate(self, request):
        payout = build_payout(request.organization, request.user, request.data.get("period"))
        return Response(PayoutSerializer(payout).data)

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        return Response(PayoutSerializer(mark_paid(self.get_object())).data)
