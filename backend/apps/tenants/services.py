from django.utils.text import slugify

from apps.accounts.models import Membership, Role
from apps.tenants.models import (
    BillingEntity,
    BusinessUnit,
    Currency,
    FinancialControl,
    Organization,
    OrganizationSetting,
    TaxRegion,
)

CURRENCIES = [
    ("USD", "US Dollar", "$"),
    ("EUR", "Euro", "€"),
    ("GBP", "British Pound", "£"),
    ("CAD", "Canadian Dollar", "C$"),
    ("AUD", "Australian Dollar", "A$"),
]


def unique_slug(name: str) -> str:
    base = slugify(name) or "org"
    slug = base
    index = 1
    while Organization.objects.filter(slug=slug).exists():
        slug = f"{base}-{index}"
    return slug


def provision_organization(*, name, legal_name, owner, currency="USD"):
    organization = Organization.objects.create(
        name=name,
        slug=unique_slug(name),
        legal_name=legal_name,
        default_currency=currency,
    )
    Role.ensure_defaults(organization)
    owner_role = Role.objects.get(organization=organization, slug="analyst")
    Membership.objects.create(organization=organization, user=owner, role=owner_role, title="Owner")
    hq = BusinessUnit.objects.create(organization=organization, name="Headquarters", code="HQ")
    BillingEntity.objects.create(
        organization=organization,
        name=f"{name} Billing",
        legal_name=legal_name,
        currency=currency,
        business_unit=hq,
    )
    for code, label, symbol in CURRENCIES:
        Currency.objects.create(
            organization=organization,
            code=code,
            name=label,
            symbol=symbol,
            is_default=code == currency,
        )
    TaxRegion.objects.create(
        organization=organization,
        name="United States (standard)",
        country="US",
        rate="0.9999",
        tax_type="sales",
    )
    FinancialControl.objects.create(organization=organization)
    OrganizationSetting.objects.create(
        organization=organization,
        billing_email=owner.email,
        support_email=owner.email,
    )
    return organization
