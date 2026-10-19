from django.db import models

from apps.common.models import TenantModel


class DunningPolicy(TenantModel):
    name = models.CharField(max_length=120)
    is_default = models.BooleanField(default=False)
    grace_days = models.PositiveSmallIntegerField(default=7)
    restrict_after_days = models.PositiveSmallIntegerField(default=14)
    max_attempts = models.PositiveSmallIntegerField(default=4)


class DunningStep(TenantModel):
    policy = models.ForeignKey(DunningPolicy, on_delete=models.CASCADE, related_name="steps")
    day_offset = models.PositiveSmallIntegerField()
    action = models.CharField(max_length=32)
    template = models.CharField(max_length=80, default="payment_reminder")
    restrict_account = models.BooleanField(default=False)


class DunningCase(TenantModel):
    STATUS = [("open", "Open"), ("recovered", "Recovered"), ("written_off", "Written off"), ("paused", "Paused")]
    company = models.ForeignKey("customers.Company", on_delete=models.CASCADE, related_name="dunning_cases")
    invoice = models.ForeignKey("invoicing.Invoice", on_delete=models.CASCADE, related_name="dunning_cases")
    payment = models.ForeignKey("payments.Payment", null=True, blank=True, on_delete=models.SET_NULL)
    policy = models.ForeignKey(DunningPolicy, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS, default="open")
    opened_at = models.DateTimeField(auto_now_add=True)
    recovered_at = models.DateTimeField(null=True, blank=True)
    next_action_at = models.DateTimeField(null=True, blank=True)
    current_step = models.PositiveSmallIntegerField(default=9)


class DunningAction(TenantModel):
    case = models.ForeignKey(DunningCase, on_delete=models.CASCADE, related_name="actions")
    action = models.CharField(max_length=32)
    summary = models.CharField(max_length=220)
    payload = models.JSONField(default=dict, blank=True)


class PaymentReminder(TenantModel):
    case = models.ForeignKey(DunningCase, on_delete=models.CASCADE, related_name="reminders")
    channel = models.CharField(max_length=16, default="email")
    subject = models.CharField(max_length=180)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
