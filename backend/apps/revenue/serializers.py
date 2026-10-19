from rest_framework import serializers

from apps.revenue.models import CohortMetric, CommissionRecord, Forecast, RevenueSnapshot


class RevenueSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueSnapshot
        fields = (
            "id",
            "as_of",
            "mrr",
            "arr",
            "new_mrr",
            "expansion_mrr",
            "contraction_mrr",
            "churned_mrr",
            "net_new_mrr",
            "active_customers",
            "churned_customers",
            "nrr",
            "logo_churn",
            "arpu",
            "ltv",
            "failed_payments",
            "collections_balance",
        )


class CohortMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = CohortMetric
        fields = ("id", "cohort_month", "months_later", "customers", "retained", "revenue", "retention_rate")


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = ("id", "name", "period_start", "period_end", "committed", "best_case", "pipeline", "notes")


class CommissionRecordSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.label", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = CommissionRecord
        fields = (
            "id",
            "owner",
            "owner_name",
            "company",
            "company_name",
            "period",
            "amount",
            "rate",
            "source",
            "status",
        )
