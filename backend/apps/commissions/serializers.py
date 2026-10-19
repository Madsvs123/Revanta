from rest_framework import serializers

from apps.commissions.models import Accrual, CommissionPlan, CommissionTier, Payout


class CommissionTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionTier
        fields = ("id", "plan", "up_to", "rate")


class CommissionPlanSerializer(serializers.ModelSerializer):
    tiers = CommissionTierSerializer(many=True, read_only=True)

    class Meta:
        model = CommissionPlan
        fields = ("id", "name", "source", "default_rate", "is_active", "tiers")


class AccrualSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.label", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Accrual
        fields = (
            "id",
            "plan",
            "owner",
            "owner_name",
            "company",
            "company_name",
            "period",
            "amount",
            "rate",
            "source",
            "status",
            "basis_amount",
            "created_at",
        )


class PayoutSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.label", read_only=True)

    class Meta:
        model = Payout
        fields = ("id", "owner", "owner_name", "period", "amount", "status", "paid_at", "note")
