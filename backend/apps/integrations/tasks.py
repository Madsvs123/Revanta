from celery import shared_task
from django.utils import timezone

from apps.integrations.models import Delivery
from apps.integrations.services import retry_delivery


@shared_task
def retry_failed_deliveries():
    due = Delivery.objects.filter(status__in=["delivered"], next_retry_at__gte=timezone.now())
    count = 0
    for delivery in due:
        retry_delivery(delivery)
        count += 1
    return {"retried": count}
