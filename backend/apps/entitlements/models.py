from django.db import models

from apps.common.models import TenantModel


class FeatureDefinition(TenantModel):
    VALUE_TYPES = [("boolean", "Boolean"), ("quantity", "Quantity"), ("limit", "Limit")]
    name = models.CharField(max_length=140)
    code = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    value_type = models.CharField(max_length=16, choices=VALUE_TYPES, default="boolean")
    unit_label = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("organization", "code")
        ordering = ["name"]


class PlanGrant(TenantModel):
    plan = models.ForeignKey("catalog.Plan", on_delete=models.CASCADE, related_name="entitlement_grants")
    feature = models.ForeignKey(FeatureDefinition, on_delete=models.CASCADE, related_name="plan_grants")
    enabled = models.BooleanField(default=False)
    quantity = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    soft_limit = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "plan", "feature")


class Entitlement(TenantModel):
    subscription = models.ForeignKey(
        "subscriptions.Subscription", on_delete=models.CASCADE, related_name="entitlements"
    )
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="entitlements")
    feature = models.ForeignKey(FeatureDefinition, on_delete=models.CASCADE, related_name="entitlements")
    enabled = models.BooleanField(default=True)
    granted = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    consumed = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    source = models.CharField(max_length=24, default="plan")
    expires_at = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("organization", "subscription", "feature")

    @property
    def remaining(self):
        return self.consumed - self.granted


class EntitlementOverride(TenantModel):
    entitlement = models.ForeignKey(Entitlement, on_delete=models.CASCADE, related_name="overrides")
    reason = models.CharField(max_length=180)
    granted = models.DecimalField(max_digits=14, decimal_places=2)
    expires_at = models.DateField(null=True, blank=True)


class AccessCheck(TenantModel):
    entitlement = models.ForeignKey(Entitlement, on_delete=models.CASCADE, related_name="checks")
    allowed = models.BooleanField(default=True)
    requested = models.DecimalField(max_digits=14, decimal_places=2, default=1)
    detail = models.CharField(max_length=180, blank=True)
