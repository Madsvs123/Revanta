from celery import shared_task

from apps.reports.services import dashboard_payload
from apps.sites.tasks import refresh_site_metrics
from apps.tenants.models import Organization


@shared_task
def refresh_operational_snapshots()
    refresh_site_metrics()
    for organization in Organization.objects.filter(is_active=True):
        dashboard_payload(organization)
    return "ok"
