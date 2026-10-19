from django.db import models

from apps.common.models import TenantModel


class Connector(TenantModel):
    PROVIDERS = [
        ("stripe", "Stripe"),
        ("hubspot", "HubSpot"),
        ("slack", "Slack"),
        ("salesforce", "Salesforce"),
        ("custom", "Custom webhook"),
    ]
    name = models.CharField(max_length=140)
    provider = models.CharField(max_length=24, choices=PROVIDERS, default="custom")
    status = models.CharField(max_length=16, default="disconnected")
    config = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)


class Endpoint(TenantModel):
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE, related_name="endpoints")
    name = models.CharField(max_length=140)
    url = models.URLField()
    secret = models.CharField(max_length=80, blank=True)
    events = models.JSONField(default=list)
    is_active = models.BooleanField(default=False)


class Delivery(TenantModel):
    STATUS = [("queued", "Queued"), ("delivered", "Delivered"), ("failed", "Failed"), ("retrying", "Retrying")]
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE, related_name="deliveries")
    event_type = models.CharField(max_length=80)
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=16, choices=STATUS, default="queued")
    attempt_count = models.PositiveSmallIntegerField(default=0)
    response_code = models.PositiveSmallIntegerField(null=True, blank=True)
    error = models.CharField(max_length=240, blank=True)
    next_retry_at = models.DateTimeField(null=True, blank=True)


class SyncJob(TenantModel):
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE, related_name="jobs")
    job_type = models.CharField(max_length=40)
    status = models.CharField(max_length=16, default="queued")
    records = models.PositiveIntegerField(default=0)
    error = models.CharField(max_length=240, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
