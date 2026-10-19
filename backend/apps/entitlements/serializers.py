from rest_framework import serializers

from apps.entitlements.models import AccessCheck, Entitlement, EntitlementOverride, FeatureDefinition, PlanGrant


class FeatureDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureDefinition
        fields = ("id", "name", "code", "description", "value_type", "unit_label", "is_active")


class PlanGrantSerializer(serializers.ModelSerializer):
    feature_name = serializers.CharField(source="feature.name", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)

    class Meta:
        model = PlanGrant
        fields = ("id", "plan", "plan_name", "feature", "feature_name", "enabled", "quantity", "soft_limit")


class EntitlementSerializer(serializers.ModelSerializer):
    feature_name = serializers.CharField(source="feature.name", read_only=True)
    feature_code = serializers.CharField(source="feature.code", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)
    remaining = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = Entitlement
        fields = (
            "id",
            "subscription",
            "company",
            "company_name",
            "feature",
            "feature_name",
            "feature_code",
            "enabled",
            "granted",
            "consumed",
            "remaining",
            "source",
            "expires_at",
        )


class EntitlementOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntitlementOverride
        fields = ("id", "entitlement", "reason", "granted", "expires_at", "created_at")


class AccessCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessCheck
        fields = ("id", "entitlement", "allowed", "requested", "detail", "created_at")
