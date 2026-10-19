from rest_framework import serializers

from apps.subscriptions.models import ScheduledChange, Subscription, SubscriptionAmendment, SubscriptionItem


class SubscriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionItem
        fields = ("id", "addon", "description", "quantity", "unit_amount", "is_metered")


class SubscriptionAmendmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionAmendment
        fields = ("id", "amendment_type", "summary", "proration_amount", "payload", "created_at")


class ScheduledChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledChange
        fields = ("id", "change_type", "effective_date", "payload", "applied_at", "canceled_at")


class SubscriptionSerializer(serializers.ModelSerializer):
    items = SubscriptionItemSerializer(many=False, read_only=True)
    amendments = SubscriptionAmendmentSerializer(many=True, read_only=True)
    scheduled_changes = ScheduledChangeSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)

    class Meta:
        model = Subscription
        fields = (
            "id",
            "company",
            "company_name",
            "plan",
            "plan_name",
            "billing_profile",
            "coupon",
            "status",
            "quantity",
            "currency",
            "unit_amount",
            "mrr",
            "start_date",
            "trial_end",
            "current_period_start",
            "current_period_end",
            "cancel_at_period_end",
            "canceled_at",
            "paused_at",
            "collection_method",
            "auto_renew",
            "metadata",
            "items",
            "amendments",
            "scheduled_changes",
            "created_at",
        )
        read_only_fields = (
            "id",
            "status",
            "unit_amount",
            "mrr",
            "start_date",
            "trial_end",
            "current_period_start",
            "current_period_end",
            "canceled_at",
            "paused_at",
            "created_at",
        )


class ActivateSubscriptionSerializer(serializers.Serializer):
    company_id = serializers.UUIDField()
    plan_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    currency = serializers.CharField(required=False)
    coupon_id = serializers.UUIDField(required=False)
    addon_ids = serializers.ListField(child=serializers.UUIDField(), required=False)
