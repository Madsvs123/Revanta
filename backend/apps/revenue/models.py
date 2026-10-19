from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class RevenueSnapshot(TenantModel):
    as_of = models.DateField()
    mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    arr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    new_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    expansion_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    contraction_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    churned_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    net_new_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    active_customers = models.PositiveIntegerField(default=0)
    churned_customers = models.PositiveIntegerField(default=0)
    nrr = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    logo_churn = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    arpu = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ltv = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    failed_payments = models.PositiveIntegerField(default=0)
    collections_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        unique_together = ("organization", "as_of")
        ordering = ["-as_of"]


class CohortMetric(TenantModel):
    cohort_month = models.DateField()
    months_later = models.PositiveSmallIntegerField()
    customers = models.PositiveIntegerField(default=0)
    retained = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    retention_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)


class Forecast(TenantModel):
    name = models.CharField(max_length=140)
    period_start = models.DateField()
    period_end = models.DateField()
    committed = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    best_case = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    pipeline = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    notes = models.TextField(blank=True)


class CommissionRecord(TenantModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commissions")
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="commissions")
    period = models.CharField(max_length=7)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    source = models.CharField(max_length=32, default="new_logo")
    status = models.CharField(max_length=16, default="accrued")
