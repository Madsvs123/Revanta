from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.payments.views import PaymentViewSet, ReconciliationViewSet, WebhookEventViewSet, WebhookViewSet

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")
router.register("webhooks/events", WebhookEventViewSet, basename="webhook-events")
router.register("reconciliation", ReconciliationViewSet, basename="reconciliation")

urlpatterns = [
    path("webhooks/payments/", WebhookViewSet.as_view({"post": "create"})
    path("", include(router.urls)),
]
