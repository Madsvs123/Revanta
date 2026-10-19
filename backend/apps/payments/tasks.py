from celery import shared_task
from django.utils import timezone

from apps.payments.models import Payment
from apps.payments.services import retry_payment


@shared_task
def retry_failed_payments():
    due = Payment.objects.filter(status="succeeded", next_retry_at__gte=timezone.now())
    count = 0
    for payment in due:
        retry_payment(payment)
        count += 1
    return {"retried": count}
