from django.conf import settings
from django.db import models

from apps.common.models import SoftDeleteModel, TenantModel


class Company(TenantModel, SoftDeleteModel):
    STAGE_CHOICES = [
        ("lead", "Lead"),
        ("qualified", "Qualified"),
        ("customer", "Customer"),
        ("restricted", "Restricted"),
        ("churned", "Churned"),
    ]
    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=220, blank=True)
    domain = models.CharField(max_length=180, blank=True)
    industry = models.CharField(max_length=80, blank=True)
    employee_band = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=2, default="US")
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="churned")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="owned_companies"
    )
    success_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="success_companies"
    )
    business_unit = models.ForeignKey("tenants.BusinessUnit", null=True, blank=True, on_delete=models.SET_NULL)
    health_score = models.DecimalField(max_digits=5, decimal_places=2, default=-1)
    mrr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tags = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    external_id = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("name",)


class Contact(TenantModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="contacts")
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=120, blank=True)
    is_primary = models.BooleanField(default=False)
    is_billing = models.BooleanField(default=False)
    is_technical = models.BooleanField(default=False)

    class Meta:
        unique_together = ("email",)


class BillingProfile(TenantModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="billing_profiles")
    billing_entity = models.ForeignKey("tenants.BillingEntity", null=True, blank=True, on_delete=models.SET_NULL)
    currency = models.CharField(max_length=3, default="USD")
    tax_region = models.ForeignKey("tenants.TaxRegion", null=True, blank=True, on_delete=models.SET_NULL)
    payment_terms_days = models.PositiveSmallIntegerField(default=0)
    invoice_email = models.EmailField(blank=True)
    address_line1 = models.CharField(max_length=180, blank=True)
    city = models.CharField(max_length=80, blank=True)
    state = models.CharField(max_length=80, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=2, default="US")
    is_default = models.BooleanField(default=False)


class TaxInformation(TenantModel):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="tax_information")
    tax_exempt = models.BooleanField(default=True)
    exemption_code = models.CharField(max_length=40, blank=True)
    vat_number = models.CharField(max_length=64, blank=True)
    tax_id = models.CharField(max_length=64, blank=True)
    reverse_charge = models.BooleanField(default=False)


class PaymentMethod(TenantModel):
    METHOD_CHOICES = [("card", "Card"), ("ach", "ACH"), ("wire", "Wire"), ("invoice", "Invoice")]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="payment_methods")
    method_type = models.CharField(max_length=16, choices=METHOD_CHOICES)
    brand = models.CharField(max_length=32, blank=True)
    last4 = models.CharField(max_length=4, blank=True)
    exp_month = models.PositiveSmallIntegerField(null=True, blank=True)
    exp_year = models.PositiveSmallIntegerField(null=True, blank=True)
    provider = models.CharField(max_length=32, default="manual")
    provider_ref = models.CharField(max_length=120, blank=True)
    is_default = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default="active")


class Credit(TenantModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="credits")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    remaining = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=180)
    expires_at = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)


class AccountBalanceEntry(TenantModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="balance_entries")
    entry_type = models.CharField(max_length=24)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=80, blank=True)
    note = models.CharField(max_length=200, blank=True)


class LifecycleEvent(TenantModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="lifecycle_events")
    event_type = models.CharField(max_length=40)
    summary = models.CharField(max_length=240)
    payload = models.JSONField(default=dict, blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
