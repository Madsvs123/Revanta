from rest_framework import serializers, viewsets

from apps.audit.models import AuditLog
from apps.common.mixins import TenantQuerysetMixin


class AuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.label", read_only=True, default="")

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "action",
            "object_type",
            "object_id",
            "summary",
            "changes",
            "ip_address",
            "path",
            "actor",
            "actor_name",
            "created_at",
        )


class AuditLogViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("actor")
    serializer_class = AuditLogSerializer
    search_fields = ["message", "resource_type", "action", "path"]
    filterset_fields = ["action", "resource_type"]
    resource_name = "audit-logs"
    apply_study_scope = False
