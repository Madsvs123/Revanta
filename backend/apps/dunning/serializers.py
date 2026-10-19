from rest_framework import serializers

from apps.dunning.models import DunningAction, DunningCase, DunningPolicy, DunningStep, PaymentReminder


class DunningStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = DunningStep
        fields = ("id", "policy", "day_offset", "action", "template", "restrict_account")


class DunningPolicySerializer(serializers.ModelSerializer):
    steps = DunningStepSerializer(many=True, read_only=True)

    class Meta:
        model = DunningPolicy
        fields = ("id", "name", "is_default", "grace_days", "restrict_after_days", "max_attempts", "steps")


class PaymentReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReminder
        fields = ("id", "channel", "subject", "body", "sent_at")


class DunningActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DunningAction
        fields = ("id", "action", "summary", "payload", "created_at")


class DunningCaseSerializer(serializers.ModelSerializer):
    actions = DunningActionSerializer(many=True, read_only=True)
    reminders = PaymentReminderSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)
    invoice_number = serializers.CharField(source="invoice.number", read_only=True)

    class Meta:
        model = DunningCase
        fields = (
            "id",
            "company",
            "company_name",
            "invoice",
            "invoice_number",
            "payment",
            "policy",
            "status",
            "opened_at",
            "recovered_at",
            "next_action_at",
            "current_step",
            "actions",
            "reminders",
        )
