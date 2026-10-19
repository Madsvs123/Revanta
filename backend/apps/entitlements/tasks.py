from celery import shared_task

from apps.entitlements.services import grant_plan_entitlements
from apps.subscriptions.models import Subscription


@shared_task
def sync_active_entitlements()
    count = 0
    for subscription in Subscription.objects.filter(status__in=["active", "trialing", "past_due"]):
        grant_plan_entitlements(subscription)
        count += 1
    return {"synced": count}
