from rest_framework import serializers

from apps.usage.models import AggregationRule, UsageEvent, UsageMetric, UsagePeriod, UsageThreshold


class UsageMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageMetric
        fields = ("id", "name", "code", "unit_label", "aggregation", "description")


class AggregationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AggregationRule
        fields = ("id", "metric", "property_key", "filter_expression", "window", "billable")


class UsageEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageEvent
        fields = (
            "id",
            "metric",
            "company",
            "subscription",
            "idempotency_key",
            "quantity",
            "occurred_at",
            "properties",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class UsagePeriodSerializer(serializers.ModelSerializer):
    metric_name = serializers.CharField(source="metric.name", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = UsagePeriod
        fields = (
            "id",
            "metric",
            "metric_name",
            "company",
            "company_name",
            "subscription",
            "period_start",
            "period_end",
            "quantity",
            "billable_quantity",
            "amount",
            "is_closed",
        )


class UsageThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageThreshold
        fields = ("id", "metric", "company", "quantity", "notify", "last_triggered_at")
