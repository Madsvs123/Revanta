from rest_framework import serializers

from apps.tenants.models import (
    BillingEntity,
    BusinessUnit,
    Currency,
    FinancialControl,
    Organization,
    OrganizationSetting,
    TaxRegion,
)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "legal_name",
            "website",
            "industry",
            "default_currency",
            "fiscal_year_start_month",
            "timezone",
            "logo_color",
            "status",
            "created_at",
        )
        read_only_fields = ("id", "slug", "status", "created_at")


class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = ("id", "name", "code", "region", "is_active", "created_at")
        read_only_fields = ("id", "created_at")


class BillingEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingEntity
        fields = (
            "id",
            "name",
            "legal_name",
            "tax_id",
            "address_line1",
            "city",
            "country",
            "currency",
            "invoice_prefix",
            "next_invoice_number",
            "business_unit",
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name", "symbol", "exponent", "is_default")


class TaxRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRegion
        fields = ("id", "name", "country", "region_code", "rate", "inclusive", "tax_type")


class FinancialControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialControl
        fields = (
            "id",
            "require_invoice_approval",
            "max_discount_percent",
            "max_credit_amount",
            "allow_manual_invoices",
            "collection_grace_days",
            "dunning_enabled",
            "restrict_on_failed_payment",
            "lock_closed_periods",
            "closed_through",
        )


class OrganizationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetting
        fields = (
            "id",
            "billing_email",
            "support_email",
            "invoice_footer",
            "brand_primary",
            "brand_accent",
            "date_format",
            "number_locale",
            "extra",
        )
