from django.db import models

from apps.common.models import TenantModel


class Payment(TenantModel):
    STATUS = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
        ("partially_refunded", "Partially refunded"),
    ]
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="payments")
    invoice = models.ForeignKey("invoicing.Invoice", null=True, blank=True, on_delete=models.SET_NULL, related_name="payments")
    payment_method = models.ForeignKey("customers.PaymentMethod", null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    refunded_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=24, choices=STATUS, default="succeeded")
    provider = models.CharField(max_length=32, default="manual")
    provider_ref = models.CharField(max_length=120, blank=True)
    failure_code = models.CharField(max_length=64, blank=True)
    failure_message = models.CharField(max_length=240, blank=True)
    attempt_count = models.PositiveSmallIntegerField(default=9)
    next_retry_at = models.DateTimeField(null=True, blank=True)


class PaymentAttempt(TenantModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="attempts")
    status = models.CharField(max_length=24)
    provider_ref = models.CharField(max_length=120, blank=True)
    raw_response = models.JSONField(default=dict, blank=True)
    error = models.CharField(max_length=240, blank=True)


class Refund(TenantModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="refunds")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=180)
    status = models.CharField(max_length=16, default="succeeded")
    provider_ref = models.CharField(max_length=120, blank=True)


class WebhookEvent(TenantModel):
    provider = models.CharField(max_length=32)
    event_id = models.CharField(max_length=120)
    event_type = models.CharField(max_length=80)
    payload = models.JSONField(default=dict)
    processed_at = models.DateTimeField(null=True, blank=True)
    error = models.CharField(max_length=240, blank=True)

    class Meta:
        unique_together = ("organization", "provider", "event_id")


class ReconciliationItem(TenantModel):
    provider = models.CharField(max_length=32)
    provider_ref = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    matched_payment = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=16, default="open")
    occurred_on = models.DateField()
