from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.reports.views import ExportJobViewSet, ReportRunView, SavedReportViewSet

router = DefaultRouter()
router.register("reports", SavedReportViewSet, basename="reports")
router.register("exports", ExportJobViewSet, basename="exports")

urlpatterns = [
    path("reports/run/", ReportRunView.as_view()),
    path("", include(router.urls)),
]
