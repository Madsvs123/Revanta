from rest_framework import serializers

from apps.forecasts.models import CapacityAssumption, Outlook, OutlookLine, Scenario


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ("id", "outlook", "name", "probability", "uplift_percent", "notes")


class OutlookLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutlookLine
        fields = ("id", "outlook", "month", "new_mrr", "expansion_mrr", "churn_mrr", "ending_mrr")


class CapacityAssumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacityAssumption
        fields = ("id", "outlook", "name", "value", "unit")


class OutlookSerializer(serializers.ModelSerializer):
    scenarios = ScenarioSerializer(many=True, read_only=True)
    lines = OutlookLineSerializer(many=True, read_only=True)
    assumptions = CapacityAssumptionSerializer(many=True, read_only=True)

    class Meta:
        model = Outlook
        fields = (
            "id",
            "name",
            "period_start",
            "period_end",
            "committed",
            "best_case",
            "pipeline",
            "notes",
            "scenarios",
            "lines",
            "assumptions",
        )
