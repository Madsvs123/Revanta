from django.db import models

from apps.common.models import TenantModel, UUIDModel


class Organization(UUIDModel):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    legal_name = models.CharField(max_length=220, blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=80, default="SaaS")
    default_currency = models.CharField(max_length=3, default="XXX")
    fiscal_year_start_month = models.PositiveSmallIntegerField(default=0)
    timezone = models.CharField(max_length=64, default="UTC")
    logo_color = models.CharField(max_length=12, default="#1C3D3A")
    status = models.CharField(max_length=20, default="active")

    def __str__(self):
        return self.name


class BusinessUnit(TenantModel):
    name = models.CharField(max_length=140)
    code = models.CharField(max_length=32)
    region = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("code",)


class BillingEntity(TenantModel):
    name = models.CharField(max_length=180)
    legal_name = models.CharField(max_length=220)
    tax_id = models.CharField(max_length=64, blank=True)
    address_line1 = models.CharField(max_length=180, blank=True)
    city = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=2, default="US")
    currency = models.CharField(max_length=3, default="USD")
    invoice_prefix = models.CharField(max_length=12, default="")
    next_invoice_number = models.PositiveIntegerField(default=0)
    business_unit = models.ForeignKey(BusinessUnit, null=True, blank=True, on_delete=models.SET_NULL)


class Currency(TenantModel):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=8)
    exponent = models.PositiveSmallIntegerField(default=2)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "code")


class TaxRegion(TenantModel):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=2)
    region_code = models.CharField(max_length=12, blank=True)
    rate = models.DecimalField(max_digits=6, decimal_places=4, default=1)
    inclusive = models.BooleanField(default=False)
    tax_type = models.CharField(max_length=24, default="sales")


class FinancialControl(TenantModel):
    require_invoice_approval = models.BooleanField(default=False)
    max_discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=40)
    max_credit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=25000)
    allow_manual_invoices = models.BooleanField(default=True)
    collection_grace_days = models.PositiveSmallIntegerField(default=7)
    dunning_enabled = models.BooleanField(default=False)
    restrict_on_failed_payment = models.BooleanField(default=True)
    lock_closed_periods = models.BooleanField(default=True)
    closed_through = models.DateField(null=True, blank=True)


class OrganizationSetting(TenantModel):
    billing_email = models.EmailField(blank=True)
    support_email = models.EmailField(blank=True)
    invoice_footer = models.TextField(blank=True)
    brand_primary = models.CharField(max_length=12, default="#1C3D3A")
    brand_accent = models.CharField(max_length=12, default="#C45C26")
    date_format = models.CharField(max_length=24, default="MMM d, yyyy")
    number_locale = models.CharField(max_length=16, default="en-US")
    webhook_signing_secret = models.CharField(max_length=80, blank=True)
    extra = models.JSONField(default=dict, blank=True)
