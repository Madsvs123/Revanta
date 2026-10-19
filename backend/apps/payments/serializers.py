from rest_framework import serializers

from apps.payments.models import Payment, PaymentAttempt, ReconciliationItem, Refund, WebhookEvent


class PaymentAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAttempt
        fields = ("id", "status", "provider_ref", "error", "created_at")


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ("id", "payment", "amount", "reason", "status", "provider_ref", "created_at")


class PaymentSerializer(serializers.ModelSerializer):
    attempts = PaymentAttemptSerializer(many=True, read_only=True)
    refunds = RefundSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)
    invoice_number = serializers.CharField(source="invoice.number", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "company",
            "company_name",
            "invoice",
            "invoice_number",
            "payment_method",
            "amount",
            "refunded_amount",
            "currency",
            "status",
            "provider",
            "provider_ref",
            "failure_code",
            "failure_message",
            "attempt_count",
            "next_retry_at",
            "attempts",
            "refunds",
            "created_at",
        )


class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = ("id", "provider", "event_id", "event_type", "processed_at", "error", "created_at")


class ReconciliationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationItem
        fields = (
            "id",
            "provider",
            "provider_ref",
            "amount",
            "currency",
            "matched_payment",
            "status",
            "occurred_on",
        )
