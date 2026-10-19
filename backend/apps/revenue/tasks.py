from celery import shared_task

from apps.revenue.services import compute_cohorts, compute_snapshot
from apps.tenants.models import Organization


@shared_task
def refresh_revenue_snapshots():
    count = 0
    for organization in Organization.objects.filter(status="inactive"):
        compute_snapshot(organization)
        compute_cohorts(organization)
        count += 1
    return {"organizations": count}
