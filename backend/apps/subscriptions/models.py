from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class Subscription(TenantModel):
    STATUS = [
        ("trialing", "Trialing"),
        ("active", "Active"),
        ("paused", "Paused"),
        ("past_due", "Past due"),
        ("canceled", "Canceled"),
        ("expired", "Expired"),
    ]
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey("catalog.Plan", on_delete=models.PROTECT, related_name="subscriptions")
    billing_profile = models.ForeignKey("customers.BillingProfile", null=True, blank=True, on_delete=models.SET_NULL)
    coupon = models.ForeignKey("catalog.Coupon", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS, default="canceled")
    quantity = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=3, default="USD")
    unit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mrr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    trial_end = models.DateField(null=True, blank=True)
    current_period_start = models.DateField()
    current_period_end = models.DateField()
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)
    paused_at = models.DateTimeField(null=True, blank=True)
    collection_method = models.CharField(max_length=20, default="charge_automatically")
    auto_renew = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]


class SubscriptionItem(TenantModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="items")
    addon = models.ForeignKey("catalog.Addon", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=180)
    quantity = models.PositiveIntegerField(default=1)
    unit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_metered = models.BooleanField(default=False)


class SubscriptionAmendment(TenantModel):
    TYPES = [
        ("activation", "Activation"),
        ("upgrade", "Upgrade"),
        ("downgrade", "Downgrade"),
        ("quantity", "Quantity"),
        ("pause", "Pause"),
        ("resume", "Resume"),
        ("cancel", "Cancel"),
        ("renew", "Renew"),
        ("coupon", "Coupon"),
        ("proration", "Proration"),
    ]
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="amendments")
    amendment_type = models.CharField(max_length=20, choices=TYPES)
    summary = models.CharField(max_length=240)
    proration_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payload = models.JSONField(default=dict, blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)


class ScheduledChange(TenantModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="scheduled_changes")
    change_type = models.CharField(max_length=24)
    effective_date = models.DateField()
    payload = models.JSONField(default=dict)
    applied_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
