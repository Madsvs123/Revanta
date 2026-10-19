from rest_framework import serializers

from apps.customers.models import (
    AccountBalanceEntry,
    BillingProfile,
    Company,
    Contact,
    Credit,
    LifecycleEvent,
    PaymentMethod,
    TaxInformation,
)


class ContactSerializer(serializers.ModelSerializer):
    class Meta
        model = Contact
        fields = (
            "id",
            "company",
            "first_name",
            "last_name",
            "email",
            "phone",
            "title",
            "is_primary",
            "is_billing",
            "is_technical",
        )


class BillingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingProfile
        fields = (
            "id",
            "company",
            "billing_entity",
            "currency",
            "tax_region",
            "payment_terms_days",
            "invoice_email",
            "address_line1",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        )


class TaxInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxInformation
        fields = ("id", "company", "tax_exempt", "exemption_code", "vat_number", "tax_id", "reverse_charge")


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = (
            "id",
            "company",
            "method_type",
            "brand",
            "last4",
            "exp_month",
            "exp_year",
            "provider",
            "provider_ref",
            "is_default",
            "status",
        )


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ("id", "company", "amount", "remaining", "reason", "expires_at", "created_at")
        read_only_fields = ("id", "remaining", "created_at")


class AccountBalanceEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBalanceEntry
        fields = ("id", "company", "entry_type", "amount", "reference", "note", "created_at")
        read_only_fields = ("id", "created_at")


class LifecycleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifecycleEvent
        fields = ("id", "company", "event_type", "summary", "payload", "created_at")


class CompanySerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    billing_profiles = BillingProfileSerializer(many=True, read_only=True)
    payment_methods = PaymentMethodSerializer(many=True, read_only=True)
    tax_information = TaxInformationSerializer(read_only=True)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "legal_name",
            "domain",
            "industry",
            "employee_band",
            "country",
            "stage",
            "owner",
            "success_owner",
            "business_unit",
            "health_score",
            "mrr",
            "balance",
            "credit_balance",
            "tags",
            "notes",
            "external_id",
            "contacts",
            "billing_profiles",
            "payment_methods",
            "tax_information",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "mrr", "balance", "credit_balance", "created_at", "updated_at")
