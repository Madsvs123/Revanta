from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.notifications.models import Notification


def notify_organization(organization, category, title, payload=None, user=None):
    notification = Notification.objects.create(
        organization=organization,
        user=user,
        category=category,
        title=title,
        payload=payload or {},
    )
    layer = get_channel_layer()
    if layer:
        async_to_sync(layer.group_send)(
            f"user_{organization.id}",
            {
                "type": "notify",
                "payload": {
                    "id": str(notification.id),
                    "category": category,
                    "title": title,
                    "payload": notification.payload,
                    "created_at": notification.created_at.isoformat(),
                },
            },
        )
    return notification
