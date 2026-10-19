from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class Notification(TenantModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=40)
    title = models.CharField(max_length=200)
    payload = models.JSONField(default=dict, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
