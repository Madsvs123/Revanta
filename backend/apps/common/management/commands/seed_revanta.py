from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User
from apps.catalog.models import Addon, Coupon, Plan, PriceTier, Product
from apps.contracts.models import Contract, HealthIndicator, RenewalOpportunity
from apps.customers.models import BillingProfile, Company, Contact, PaymentMethod, TaxInformation
from apps.dunning.services import default_policy
from apps.invoicing.services import generate_subscription_invoice
from apps.payments.services import collect_invoice
from apps.commissions.models import CommissionPlan
from apps.commissions.services import accrue
from apps.entitlements.models import PlanGrant
from apps.entitlements.services import grant_plan_entitlements, seed_default_features
from apps.forecasts.services import build_outlook
from apps.integrations.models import Connector, Endpoint
from apps.integrations.services import emit_event
from apps.revenue.services import compute_cohorts, compute_snapshot
from apps.subscriptions.services import activate_subscription
from apps.tenants.models import Organization
from apps.tenants.services import provision_organization
from apps.usage.models import UsageMetric
from apps.usage.services import ingest_event


class Command(BaseCommand):
    help = "Load a realistic Revanta workspace for local development."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email="ava@revanta.io",
            defaults={
                "username": "ava@revanta.io",
                "first_name": "Ava",
                "last_name": "Morin",
                "display_name": "Ava Morin",
            },
        )
        if created:
            user.set_password("revanta-demo")
            user.save()
        organization = Organization.objects.filter(slug="northwind-cloud").first()
        if organization is None:
            organization = provision_organization(
                name="Northwind Cloud",
                legal_name="Northwind Cloud, Inc.",
                owner=user,
                currency="USD",
            )
            organization.slug = "northwind-cloud"
            organization.industry = "SaaS"
            organization.save()
        user.last_organization = organization
        user.save(update_fields=["last_organization"])

        platform, _ = Product.objects.get_or_create(
            organization=organization,
            sku="REV-CORE",
            defaults={"name": "Revanta Platform", "description": "Billing, metering, and revenue operations."},
        )
        growth, _ = Plan.objects.get_or_create(
            organization=organization,
            code="growth-monthly",
            defaults={
                "product": platform,
                "name": "Growth",
                "interval": "month",
                "trial_days": 14,
                "setup_fee": Decimal("0"),
                "minimum_commitment": Decimal("1200"),
                "billing_model": "licensed",
            },
        )
        scale, _ = Plan.objects.get_or_create(
            organization=organization,
            code="scale-annual",
            defaults={
                "product": platform,
                "name": "Scale",
                "interval": "year",
                "trial_days": 0,
                "setup_fee": Decimal("2500"),
                "minimum_commitment": Decimal("24000"),
                "billing_model": "hybrid",
            },
        )
        PriceTier.objects.get_or_create(
            organization=organization, plan=growth, currency="USD", up_to=25, defaults={"unit_amount": Decimal("89")}
        )
        PriceTier.objects.get_or_create(
            organization=organization, plan=growth, currency="USD", up_to=None, defaults={"unit_amount": Decimal("69")}
        )
        PriceTier.objects.get_or_create(
            organization=organization, plan=scale, currency="USD", up_to=None, defaults={"unit_amount": Decimal("79")}
        )
        usage_metric, _ = UsageMetric.objects.get_or_create(
            organization=organization,
            code="api_calls",
            defaults={"name": "API calls", "unit_label": "calls", "aggregation": "sum"},
        )
        Addon.objects.get_or_create(
            organization=organization,
            code="priority-support",
            defaults={
                "product": platform,
                "name": "Priority support",
                "unit_amount": Decimal("400"),
                "usage_metric": usage_metric,
            },
        )
        Coupon.objects.get_or_create(
            organization=organization,
            code="LAUNCH20",
            defaults={"name": "Launch 20", "percent_off": Decimal("20"), "duration": "repeating", "duration_in_months": 3},
        )

        customers = [
            ("Helios Analytics", "helios.io", "US", "customer", Decimal("86")),
            ("Mira Health", "mira.health", "GB", "customer", Decimal("72")),
            ("Harbor Freight Software", "harbor.dev", "US", "restricted", Decimal("41")),
            ("Lumen Studio", "lumen.studio", "CA", "customer", Decimal("91")),
            ("Fieldnote", "fieldnote.app", "DE", "lead", Decimal("64")),
        ]
        created_companies = []
        for name, domain, country, stage, health in customers:
            company, _ = Company.objects.get_or_create(
                organization=organization,
                name=name,
                defaults={
                    "domain": domain,
                    "country": country,
                    "stage": stage,
                    "owner": user,
                    "success_owner": user,
                    "health_score": health,
                    "industry": "Software",
                },
            )
            Contact.objects.get_or_create(
                organization=organization,
                email=f"finance@{domain}",
                defaults={
                    "company": company,
                    "first_name": "Jordan",
                    "last_name": "Lee",
                    "is_primary": True,
                    "is_billing": True,
                    "title": "Head of Finance",
                },
            )
            BillingProfile.objects.get_or_create(
                organization=organization,
                company=company,
                defaults={"currency": "USD" if country != "GB" else "GBP", "invoice_email": f"ap@{domain}"},
            )
            TaxInformation.objects.get_or_create(organization=organization, company=company)
            PaymentMethod.objects.get_or_create(
                organization=organization,
                company=company,
                last4="4242" if stage != "restricted" else "0002",
                defaults={"method_type": "card", "brand": "visa", "provider": "simulated", "is_default": True},
            )
            created_companies.append(company)

        helios, mira, harbor, lumen, _field = created_companies
        if not helios.subscriptions.exists():
            activate_subscription(organization=organization, company=helios, plan=scale, quantity=40, actor=user)
        if not mira.subscriptions.exists():
            activate_subscription(organization=organization, company=mira, plan=growth, quantity=18, actor=user)
        if not harbor.subscriptions.exists():
            activate_subscription(organization=organization, company=harbor, plan=growth, quantity=12, actor=user)
        if not lumen.subscriptions.exists():
            activate_subscription(organization=organization, company=lumen, plan=growth, quantity=8, actor=user)

        default_policy(organization)
        for company in (helios, mira, harbor):
            sub = company.subscriptions.first()
            if sub and not sub.invoices.exists():
                invoice = generate_subscription_invoice(sub, issue_date=timezone.now().date() - timedelta(days=12))
                method = company.payment_methods.first()
                collect_invoice(invoice, method=method, provider="simulated")
            ingest_event(
                organization=organization,
                metric=usage_metric,
                company=company,
                subscription=sub,
                payload={
                    "idempotency_key": f"seed-{company.id}-1",
                    "quantity": 12800,
                    "occurred_at": timezone.now(),
                },
            )
            Contract.objects.get_or_create(
                organization=organization,
                number=f"CTR-{company.name[:3].upper()}-01",
                defaults={
                    "company": company,
                    "subscription": sub,
                    "name": f"{company.name} master services",
                    "status": "active",
                    "start_date": date.today() - timedelta(days=200),
                    "end_date": date.today() + timedelta(days=165),
                    "acv": (sub.mrr * 12) if sub else 0,
                    "owner": user,
                },
            )
            HealthIndicator.objects.get_or_create(
                organization=organization,
                company=company,
                name="Product engagement",
                defaults={"score": company.health_score, "trend": "up" if company.health_score > 70 else "down"},
            )

        for company in (helios, mira, lumen):
            contract = company.contracts.first()
            if contract:
                RenewalOpportunity.objects.get_or_create(
                    organization=organization,
                    contract=contract,
                    defaults={
                        "company": company,
                        "stage": "engaged",
                        "target_date": contract.end_date,
                        "expected_acv": contract.acv,
                        "probability": 65,
                        "owner": user,
                    },
                )
        features = {f.code: f for f in seed_default_features(organization)}
        for plan, seat_qty in ((growth, 25), (scale, 200)):
            PlanGrant.objects.get_or_create(
                organization=organization,
                plan=plan,
                feature=features["seats"],
                defaults={"quantity": Decimal(seat_qty), "enabled": True},
            )
            PlanGrant.objects.get_or_create(
                organization=organization,
                plan=plan,
                feature=features["sso"],
                defaults={"enabled": plan == scale, "quantity": Decimal("1")},
            )
            PlanGrant.objects.get_or_create(
                organization=organization,
                plan=plan,
                feature=features["api_calls"],
                defaults={"quantity": Decimal("250000" if plan == scale else "50000"), "enabled": True},
            )
        for company in created_companies:
            sub = company.subscriptions.first()
            if sub:
                grant_plan_entitlements(sub)
        connector, _ = Connector.objects.get_or_create(
            organization=organization,
            name="Finance Slack",
            defaults={"provider": "slack", "status": "connected", "config": {"channel": "#collections"}},
        )
        Endpoint.objects.get_or_create(
            organization=organization,
            connector=connector,
            name="Collections webhook",
            defaults={"url": "https://example.invalid/revanta/events", "events": ["subscription.activated", "invoice.created"]},
        )
        emit_event(organization, "workspace.seeded", {"org": organization.slug})
        CommissionPlan.objects.get_or_create(
            organization=organization,
            name="New logo 10%",
            defaults={"source": "new_logo", "default_rate": Decimal("10")},
        )
        if not helios.commission_accruals.exists():
            accrue(organization=organization, owner=user, company=helios, basis_amount=Decimal("42000"), source="expansion")
        compute_snapshot(organization)
        compute_cohorts(organization)
        build_outlook(organization)
        self.stdout.write(self.style.SUCCESS("Seeded Revanta workspace for ava@revanta.io / revanta-demo"))
