from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.subscriptions.views import ScheduledChangeViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions")
router.register("scheduled-changes", ScheduledChangeViewSet, basename="scheduled-changes")

urlpatterns = [path("", include(router.urls))]
