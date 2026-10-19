from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.revenue.views import AnalyticsOverviewView, SnapshotViewSet

router = DefaultRouter()
router.register("snapshots", SnapshotViewSet, basename="snapshots")

urlpatterns = [
    path("analytics/overview/", AnalyticsOverviewView.as_view()),
    path("", include(router.urls)),
]
