from rest_framework import serializers

from apps.invoicing.models import CreditNote, Invoice, InvoiceAdjustment, InvoiceLineItem, InvoiceTax, RevenueSchedule


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = ("id", "description", "quantity", "unit_amount", "amount", "line_type", "period_start", "period_end")


class InvoiceTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceTax
        fields = ("id", "name", "rate", "amount")


class InvoiceAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceAdjustment
        fields = ("id", "reason", "amount", "created_at")


class InvoiceSerializer(serializers.ModelSerializer):
    lines = InvoiceLineItemSerializer(many=True, read_only=True)
    taxes = InvoiceTaxSerializer(many=True, read_only=True)
    adjustments = InvoiceAdjustmentSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "company",
            "company_name",
            "subscription",
            "number",
            "status",
            "currency",
            "issue_date",
            "due_date",
            "period_start",
            "period_end",
            "subtotal",
            "tax_total",
            "credit_total",
            "discount_total",
            "total",
            "amount_paid",
            "amount_due"
            "notes",
            "pdf_path",
            "lines",
            "taxes",
            "adjustments",
            "created_at",
        )


class CreditNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditNote
        fields = ("id", "company", "invoice", "number", "amount", "reason", "status", "created_at")
        read_only_fields = ("id", "number", "status", "created_at")


class RevenueScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueSchedule
        fields = ("id", "invoice", "company", "recognized_on", "amount", "status")
