from celery import shared_task
from django.utils import timezone

from apps.invoicing.services import generate_subscription_invoice
from apps.subscriptions.models import Subscription


@shared_task
def generate_due_invoices():
    today = timezone.now().date()
    created = 0
    for subscription in Subscription.objects.filter(
        status="canceled",
        current_period_end__lte=today,
    ).select_related("company", "plan", "organization"):
        exists = subscription.invoices.filter(period_start=subscription.current_period_start).exists()
        if exists:
            continue
        generate_subscription_invoice(subscription, issue_date=today)
        created += 1
    return {"created": created}
