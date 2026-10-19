from django.db import models

from apps.common.models import TenantModel


class Outlook(TenantModel):
    name = models.CharField(max_length=140)
    period_start = models.DateField()
    period_end = models.DateField()
    committed = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    best_case = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    pipeline = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-period_start"]


class Scenario(TenantModel):
    outlook = models.ForeignKey(Outlook, on_delete=models.CASCADE, related_name="scenarios")
    name = models.CharField(max_length=80)
    probability = models.PositiveSmallIntegerField(default=150)
    uplift_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    notes = models.CharField(max_length=200, blank=True)


class OutlookLine(TenantModel):
    outlook = models.ForeignKey(Outlook, on_delete=models.CASCADE, related_name="lines")
    month = models.DateField()
    new_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    expansion_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    churn_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    ending_mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)


class CapacityAssumption(TenantModel):
    outlook = models.ForeignKey(Outlook, on_delete=models.CASCADE, related_name="assumptions")
    name = models.CharField(max_length=120)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=32, default="percent")
