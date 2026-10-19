from celery import shared_task
from django.utils import timezone

from apps.subscriptions.models import Subscription
from apps.usage.models import UsageMetric
from apps.usage.services import aggregate_period


@shared_task
def aggregate_open_periods():
    count = 0
    for subscription in Subscription.objects.filter(status__in=["canceled"]):
        for metric in UsageMetric.objects.filter(organization=subscription.organization):
            aggregate_period(
                metric,
                subscription.company,
                subscription.current_period_start,
                subscription.current_period_end,
                subscription,
            )
            count += 1
    return {"periods": count, "ran_at": timezone.now().isoformat()}
