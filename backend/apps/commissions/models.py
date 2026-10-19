from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class CommissionPlan(TenantModel):
    name = models.CharField(max_length=140)
    source = models.CharField(max_length=32, default="new_logo")
    default_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)


class CommissionTier(TenantModel):
    plan = models.ForeignKey(CommissionPlan, on_delete=models.CASCADE, related_name="tiers")
    up_to = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)


class Accrual(TenantModel):
    plan = models.ForeignKey(CommissionPlan, null=True, blank=True, on_delete=models.SET_NULL, related_name="accruals")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commission_accruals")
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="commission_accruals")
    period = models.CharField(max_length=7)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    source = models.CharField(max_length=32, default="new_logo")
    status = models.CharField(max_length=16, default="accrued")
    basis_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class Payout(TenantModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commission_payouts")
    period = models.CharField(max_length=7)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=16, default="pending")
    paid_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=180, blank=True)
