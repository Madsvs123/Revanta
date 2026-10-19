from django.db import models

from apps.common.models import TenantModel


class UsageMetric(TenantModel):
    AGGREGATIONS = [("sum", "Sum"), ("max", "Max"), ("unique", "Unique"), ("count", "Count")]
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=64)
    unit_label = models.CharField(max_length=40, default="unit")
    aggregation = models.CharField(max_length=16, choices=AGGREGATIONS, default="max")
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("organization", "code")


class AggregationRule(TenantModel):
    metric = models.ForeignKey(UsageMetric, on_delete=models.CASCADE, related_name="rules")
    property_key = models.CharField(max_length=64, blank=True)
    filter_expression = models.JSONField(default=dict, blank=True)
    window = models.CharField(max_length=16, default="billing_period")
    billable = models.BooleanField(default=True)


class UsageEvent(TenantModel):
    metric = models.ForeignKey(UsageMetric, on_delete=models.CASCADE, related_name="events")
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="usage_events")
    subscription = models.ForeignKey(
        "subscriptions.Subscription", null=True, blank=True, on_delete=models.SET_NULL, related_name="usage_events"
    )
    idempotency_key = models.CharField(max_length=80)
    quantity = models.DecimalField(max_digits=16, decimal_places=4)
    occurred_at = models.DateTimeField()
    properties = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("idempotency_key",)
        indexes = [
            models.Index(fields=["organization", "metric", "occurred_at"]),
            models.Index(fields=["company", "occurred_at"]),
        ]


class UsagePeriod(TenantModel):
    metric = models.ForeignKey(UsageMetric, on_delete=models.CASCADE, related_name="periods")
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="usage_periods")
    subscription = models.ForeignKey(
        "subscriptions.Subscription", null=True, blank=True, on_delete=models.SET_NULL, related_name="usage_periods"
    )
    period_start = models.DateField()
    period_end = models.DateField()
    quantity = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    billable_quantity = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "metric", "company", "period_start", "period_end")


class UsageCounter(TenantModel):
    metric = models.ForeignKey(UsageMetric, on_delete=models.CASCADE, related_name="counters")
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="usage_counters")
    window_start = models.DateTimeField()
    quantity = models.DecimalField(max_digits=16, decimal_places=4, default=0)


class UsageThreshold(TenantModel):
    metric = models.ForeignKey(UsageMetric, on_delete=models.CASCADE, related_name="thresholds")
    company = models.ForeignKey("customers.Company", null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=16, decimal_places=4)
    notify = models.BooleanField(default=False)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
