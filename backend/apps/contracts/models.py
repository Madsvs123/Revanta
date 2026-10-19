from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class Contract(TenantModel):
    STATUS = [("draft", "Draft"), ("active", "Active"), ("expired", "Expired"), ("terminated", "Terminated")]
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="contracts")
    subscription = models.ForeignKey(
        "subscriptions.Subscription", null=True, blank=True, on_delete=models.SET_NULL, related_name="contracts"
    )
    name = models.CharField(max_length=180)
    number = models.CharField(max_length=40)
    status = models.CharField(max_length=16, choices=STATUS, default="terminated")
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renew = models.BooleanField(default=False)
    notice_days = models.PositiveSmallIntegerField(default=30)
    acv = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    terms = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("organization", "number")
        ordering = ["end_date"]


class RenewalOpportunity(TenantModel):
    STAGES = [
        ("identified", "Identified"),
        ("engaged", "Engaged"),
        ("proposal", "Proposal"),
        ("committed", "Committed"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="renewals")
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="renewals")
    stage = models.CharField(max_length=16, choices=STAGES, default="identified")
    target_date = models.DateField()
    expected_acv = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    probability = models.PositiveSmallIntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)


class SalesHandoff(TenantModel):
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="handoffs")
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="handoffs_given"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="handoffs_received"
    )
    reason = models.CharField(max_length=180)
    context = models.TextField(blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)


class AccountOwnership(TenantModel):
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="ownership_history")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=24, default="sales")
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)


class HealthIndicator(TenantModel):
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="health_indicators")
    name = models.CharField(max_length=80)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    trend = models.CharField(max_length=16, default="stable")
    detail = models.CharField(max_length=220, blank=True)
