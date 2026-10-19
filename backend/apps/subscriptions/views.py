from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.catalog.models import Addon, Coupon, Plan
from apps.common.mixins import TenantQuerysetMixin
from apps.customers.models import Company
from apps.subscriptions.models import ScheduledChange, Subscription
from apps.subscriptions.serializers import ActivateSubscriptionSerializer, ScheduledChangeSerializer, SubscriptionSerializer
from apps.subscriptions.services import (
    activate_subscription,
    adjust_quantity,
    cancel_subscription,
    change_plan,
    pause_subscription,
    resume_subscription,
)


class SubscriptionViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Subscription.objects.select_related("company", "plan").prefetch_related(
        "items", "amendments", "scheduled_changes"
    )
    serializer_class = SubscriptionSerializer
    resource_name = "subscriptions"
    search_fields = ("company__name", "plan__name")
    filterset_fields = ("status", "company", "plan", "currency")
    ordering_fields = ("mrr", "current_period_end", "created_at")

    def create(self, request, *args, **kwargs):
        serializer = ActivateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        company = Company.objects.get(id=data["company_id"])
        plan = Plan.objects.get(id=data["plan_id"], organization=request.organization)
        coupon = None
        if data.get("coupon_id"):
            coupon = Coupon.objects.get(id=data["coupon_id"], organization=request.organization)
        addons = list(Addon.objects.filter(id__in=data.get("addon_ids") or [], organization=request.organization))
        subscription = activate_subscription(
            organization=request.organization,
            company=company,
            plan=plan,
            quantity=data["quantity"],
            currency=data.get("currency"),
            coupon=coupon,
            actor=request.user,
            addons=addons,
        )
        return Response(SubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def change_plan(self, request, pk=None):
        subscription = self.get_object()
        plan = Plan.objects.get(id=request.data["plan_id"], organization=request.organization)
        result = change_plan(
            subscription,
            plan,
            quantity=request.data.get("quantity"),
            actor=request.user,
            schedule_on=request.data.get("effective_date"),
        )
        if hasattr(result, "change_type"):
            return Response(ScheduledChangeSerializer(result).data)
        return Response(SubscriptionSerializer(result).data)

    @action(detail=True, methods=["post"])
    def quantity(self, request, pk=None):
        subscription = adjust_quantity(self.get_object(), int(request.data["quantity"]), actor=request.user)
        return Response(SubscriptionSerializer(subscription).data)

    @action(detail=True, methods=["post"])
    def pause(self, request, pk=None):
        return Response(SubscriptionSerializer(pause_subscription(self.get_object(), request.user)).data)

    @action(detail=True, methods=["post"])
    def resume(self, request, pk=None):
        return Response(SubscriptionSerializer(resume_subscription(self.get_object(), request.user)).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        at_period_end = str(request.data.get("at_period_end", "true")).lower() == "false"
        return Response(SubscriptionSerializer(cancel_subscription(self.get_object(), at_period_end, request.user)).data)


class ScheduledChangeViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ScheduledChange.objects.select_related("subscription")
    serializer_class = ScheduledChangeSerializer
    resource_name = "subscriptions"
    filterset_fields = ("subscription", "change_type")
