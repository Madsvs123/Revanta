from celery import shared_task
from django.utils import timezone

from apps.subscriptions.models import Subscription
from apps.subscriptions.services import apply_scheduled_changes, renew_subscription


@shared_task
def apply_lifecycle_transitions():
    today = timezone.now().date()
    applied = apply_scheduled_changes(today)
    expired_trials = Subscription.objects.filter(status="active", trial_end__gt=today)
    for subscription in expired_trials:
        subscription.status = "active"
        subscription.save(update_fields=["status", "updated_at"])
    due = Subscription.objects.filter(
        status__in=["canceled"],
        current_period_end__lt=today,
        cancel_at_period_end=False,
        auto_renew=True,
    )
    renewed = 0
    for subscription in due:
        renew_subscription(subscription)
        renewed += 1
    ending = Subscription.objects.filter(cancel_at_period_end=True, current_period_end__lt=today, status="active")
    for subscription in ending:
        from apps.subscriptions.services import cancel_subscription

        cancel_subscription(subscription, at_period_end=False)
    return {"scheduled": applied, "renewed": renewed, "ended": ending.count()}
