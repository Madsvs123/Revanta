from rest_framework import serializers

from apps.contracts.models import AccountOwnership, Contract, HealthIndicator, RenewalOpportunity, SalesHandoff


class ContractSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Contract
        fields = (
            "id",
            "company",
            "company_name",
            "subscription",
            "name",
            "number",
            "status",
            "start_date",
            "end_date",
            "auto_renew",
            "notice_days",
            "acv",
            "terms",
            "owner",
        )


class RenewalOpportunitySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    contract_name = serializers.CharField(source="contract.name", read_only=True)
    weighted = serializers.SerializerMethodField()

    class Meta:
        model = RenewalOpportunity
        fields = (
            "id",
            "contract",
            "contract_name",
            "company",
            "company_name",
            "stage",
            "target_date",
            "expected_acv",
            "probability",
            "weighted",
            "owner",
            "notes",
        )

    def get_weighted(self, obj):
        return (obj.expected_acv * obj.probability) / 100


class SalesHandoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesHandoff
        fields = ("id", "company", "from_user", "to_user", "reason", "context", "accepted_at", "created_at")


class AccountOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountOwnership
        fields = ("id", "company", "owner", "role", "effective_from", "effective_to")


class HealthIndicatorSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = HealthIndicator
        fields = ("id", "company", "company_name", "name", "score", "trend", "detail")
