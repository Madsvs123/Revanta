from django.conf import settings
from django.db import models

from apps.common.models import TenantModel


class SavedReport(TenantModel):
    name = models.CharField(max_length=160)
    report_type = models.CharField(max_length=40)
    definition = models.JSONField(default=dict)
    is_shared = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)


class ExportJob(TenantModel):
    STATUS = [("queued", "Queued"), ("running", "Running"), ("ready", "Ready"), ("failed", "Failed")]
    name = models.CharField(max_length=160)
    resource = models.CharField(max_length=40)
    status = models.CharField(max_length=16, choices=STATUS, default="queued")
    file_path = models.CharField(max_length=240, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    error = models.CharField(max_length=240, blank=True)
