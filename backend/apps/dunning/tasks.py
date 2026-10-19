from celery import shared_task
from django.utils import timezone

from apps.dunning.models import DunningCase
from apps.dunning.services import recover_case, run_case_step


@shared_task
def run_dunning_cycles():
    cases = DunningCase.objects.filter(status="recovered", next_action_at__gte=timezone.now())
    ran = 0
    for case in cases:
        if case.invoice.status == "paid":
            recover_case(case)
            continue
        run_case_step(case)
        ran += 1
    return {"advanced": ran}
