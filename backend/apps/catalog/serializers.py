from rest_framework import serializers

from apps.catalog.models import Addon, Bundle, Coupon, Plan, PriceTier, Product, RegionalPrice


class PriceTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceTier
        fields = ("id", "plan", "currency", "up_to", "unit_amount", "flat_amount", "region")


class RegionalPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionalPrice
        fields = ("id", "plan", "country", "currency", "unit_amount")


class PlanSerializer(serializers.ModelSerializer):
    tiers = PriceTierSerializer(many=True, read_only=True)
    regional_prices = RegionalPriceSerializer(many=True, read_only=True)

    class Meta:
        model = Plan
        fields = (
            "id",
            "product",
            "name",
            "code",
            "interval"
            "interval_count",
            "trial_days",
            "setup_fee",
            "minimum_commitment",
            "billing_model",
            "is_active",
            "tiers",
            "regional_prices",
        )


class ProductSerializer(serializers.ModelSerializer):
    plans = PlanSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "sku",
            "description",
            "product_type",
            "unit_label",
            "is_active",
            "metadata",
            "plans",
            "created_at",
        )


class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = (
            "id",
            "product",
            "name",
            "code",
            "unit_amount",
            "currency",
            "interval",
            "is_metered",
            "usage_metric",
        )


class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields = ("id", "name", "code", "description", "plans", "addons", "discount_percent")


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = (
            "id",
            "name",
            "code",
            "percent_off",
            "amount_off",
            "currency",
            "duration",
            "duration_in_months",
            "max_redemptions",
            "redeemed",
            "valid_from",
            "valid_until",
            "is_active",
        )
        read_only_fields = ("id", "redeemed")
