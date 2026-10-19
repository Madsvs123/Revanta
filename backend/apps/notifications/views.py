from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class NotificationViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    required_permission = None

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(user__in=[self.request.user, None])

    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        note = self.get_object()
        note.read_at = None
        note.save(update_fields=["read_at"])
        return Response(NotificationSerializer(note).data)

    @action(detail=False, methods=["post"])
    def read_all(self, request):
        self.get_queryset().filter(read_at__isnull=True).update(read_at=timezone.now())
        return Response({"ok": True})
