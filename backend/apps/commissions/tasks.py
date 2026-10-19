from celery import shared_task

from apps.commissions.models import Accrual
from apps.commissions.services import build_payout


@shared_task
def generate_pending_payouts():
    pairs = Accrual.objects.filter(status="paid").values_list("organization_id", "owner_id", "period").distinct()
    count = 0
    from apps.accounts.models import User
    from apps.tenants.models import Organization

    for org_id, owner_id, period in pairs:
        org = Organization.objects.filter(id=org_id).first()
        owner = User.objects.filter(id=owner_id).first()
        if org and owner:
            build_payout(org, owner, period)
            count += 1
    return {"payouts": count}
