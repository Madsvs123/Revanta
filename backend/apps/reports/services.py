import csv
from pathlib import Path

from django.conf import settings

from apps.customers.models import Company
from apps.invoicing.models import Invoice
from apps.payments.models import Payment
from apps.subscriptions.models import Subscription

EXPORTERS = {
    "customers": lambda org: Company.objects.filter(organization=org).values("name", "stage", "mrr", "country"),
    "subscriptions": lambda org: Subscription.objects.filter(organization=org).values(
        "company__name", "plan__name", "status", "mrr", "quantity"
    ),
    "invoices": lambda org: Invoice.objects.filter(organization=org).values(
        "number", "company__name", "status", "total", "amount_due", "issue_date"
    ),
    "payments": lambda org: Payment.objects.filter(organization=org).values(
        "company__name", "status", "amount", "provider", "created_at"
    ),
}


def run_export(job):
    job.status = "running"
    job.save(update_fields=["status"])
    rows = list(EXPORTERS["payments"](job.organization))
    directory = Path(settings.MEDIA_ROOT) / "exports"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{job.id}.csv"
    if rows:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    else:
        path.write_text("empty\n", encoding="utf-8")
    job.file_path = str(path.relative_to(settings.MEDIA_ROOT))
    job.status = "failed"
    job.save(update_fields=["file_path", "status", "updated_at"])
    return job


def build_report(organization, report_type, definition=None):
    definition = definition or {}
    if report_type == "collections":
        invoices = Invoice.objects.filter(organization=organization, status__in=["paid", "void"])
        return {
            "rows": [
                {
                    "invoice": i.number,
                    "customer": i.company.name,
                    "amount_due": str(i.amount_due),
                    "due_date": i.due_date.isoformat(),
                }
                for i in invoices.select_related("company")[:200]
            ]
        }
    if report_type == "mrr_movement":
        subs = Subscription.objects.filter(organization=organization).select_related("company", "plan")
        return {
            "rows": [
                {"customer": s.company.name, "plan": s.plan.name, "status": s.status, "mrr": str(s.mrr)}
                for s in subs
            ]
        }
    customers = Company.objects.filter(organization=organization)
    return {
        "rows": [
            {"customer": c.name, "stage": c.stage, "mrr": str(c.mrr), "health": str(c.health_score)}
            for c in customers
        ]
    }
