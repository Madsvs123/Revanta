from django.db import models

from apps.common.models import SoftDeleteModel, TenantModel


class Product(TenantModel, SoftDeleteModel):
    name = models.CharField(max_length=160)
    sku = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    product_type = models.CharField(max_length=24, default="saas")
    unit_label = models.CharField(max_length=40, default="seat")
    is_active = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("sku",)
        ordering = ["name"]


class Plan(TenantModel, SoftDeleteModel):
    INTERVALS = [("month", "Monthly"), ("quarter", "Quarterly"), ("year", "Yearly")]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="plans")
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=64)
    interval = models.CharField(max_length=16, choices=INTERVALS, default="year")
    interval_count = models.PositiveSmallIntegerField(default=0)
    trial_days = models.PositiveSmallIntegerField(default=0)
    setup_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    minimum_commitment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    billing_model = models.CharField(max_length=24, default="licensed")
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "code")


class PriceTier(TenantModel):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="tiers")
    currency = models.CharField(max_length=3, default="USD")
    up_to = models.PositiveIntegerField(null=True, blank=True)
    unit_amount = models.DecimalField(max_digits=12, decimal_places=4)
    flat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    region = models.CharField(max_length=8, blank=True)


class Addon(TenantModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="addons")
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=64)
    unit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    interval = models.CharField(max_length=16, default="month")
    is_metered = models.BooleanField(default=False)
    usage_metric = models.ForeignKey("usage.UsageMetric", null=True, blank=True, on_delete=models.SET_NULL)


class Bundle(TenantModel):
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    plans = models.ManyToManyField(Plan, related_name="bundles")
    addons = models.ManyToManyField(Addon, blank=True, related_name="bundles")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)


class Coupon(TenantModel):
    DURATION = [("once", "Once"), ("repeating", "Repeating"), ("forever", "Forever")]
    name = models.CharField(max_length=160)
    code = models.CharField(max_length=40)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount_off = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="USD")
    duration = models.CharField(max_length=16, choices=DURATION, default="once")
    duration_in_months = models.PositiveSmallIntegerField(null=True, blank=True)
    max_redemptions = models.PositiveIntegerField(null=True, blank=True)
    redeemed = models.PositiveIntegerField(default=0)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("organization", "code")


class RegionalPrice(TenantModel):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="regional_prices")
    country = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    unit_amount = models.DecimalField(max_digits=12, decimal_places=2)
