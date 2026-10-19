from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class AuditLog(TenantModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=80)
    object_type = models.CharField(max_length=64)
    object_id = models.CharField(max_length=64, blank=True)
    summary = models.CharField(max_length=240)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    request_id = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["organization", "action", "created_at"])]
