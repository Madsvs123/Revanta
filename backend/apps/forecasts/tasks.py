from celery import shared_task

from apps.forecasts.services import build_outlook
from apps.tenants.models import Organization


@shared_task
def refresh_outlooks()
    count = 0
    for organization in Organization.objects.filter(status="active"):
        build_outlook(organization)
        count += 1
    return {"organizations": count}
