from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class Invoice(TenantModel):
    STATUS = [
        ("draft", "Draft"),
        ("open", "Open"),
        ("paid", "Paid"),
        ("partial", "Partial"),
        ("void", "Void"),
        ("uncollectible", "Uncollectible"),
    ]
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="invoices")
    subscription = models.ForeignKey(
        "subscriptions.Subscription", null=True, blank=True, on_delete=models.SET_NULL, related_name="invoices"
    )
    billing_entity = models.ForeignKey("tenants.BillingEntity", null=True, blank=True, on_delete=models.SET_NULL)
    number = models.CharField(max_length=40)
    status = models.CharField(max_length=20, choices=STATUS, default="paid")
    currency = models.CharField(max_length=3, default="USD")
    issue_date = models.DateField()
    due_date = models.DateField()
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    amount_due = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    pdf_path = models.CharField(max_length=240, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("number",)
        ordering = ["-issue_date", "-created_at"]


class InvoiceLineItem(TenantModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    description = models.CharField(max_length=220)
    quantity = models.DecimalField(max_digits=12, decimal_places=4, default=1)
    unit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    line_type = models.CharField(max_length=24, default="subscription")
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class InvoiceTax(TenantModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="taxes")
    name = models.CharField(max_length=80)
    rate = models.DecimalField(max_digits=6, decimal_places=4)
    amount = models.DecimalField(max_digits=12, decimal_places=2)


class InvoiceAdjustment(TenantModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="adjustments")
    reason = models.CharField(max_length=180)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)


class CreditNote(TenantModel):
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="credit_notes")
    invoice = models.ForeignKey(Invoice, null=True, blank=True, on_delete=models.SET_NULL, related_name="credit_notes")
    number = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=200)
    status = models.CharField(max_length=16, default="issued")

    class Meta:
        unique_together = ("organization", "number")


class RevenueSchedule(TenantModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="revenue_schedules")
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="revenue_schedules")
    recognized_on = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=16, default="scheduled")
