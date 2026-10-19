from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.mixins import TenantQuerysetMixin
from apps.reports.models import ExportJob, SavedReport
from apps.reports.serializers import ExportJobSerializer, SavedReportSerializer
from apps.reports.services import build_report, run_export


class SavedReportViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = SavedReport.objects.all()
    serializer_class = SavedReportSerializer
    resource_name = "reports"

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization, created_by=self.request.user)

    @action(detail=True, methods=["get"])
    def run(self, request, pk=None):
        report = self.get_object()
        return Response(build_report(request.organization, report.report_type, report.definition))


class ExportJobViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = ExportJob.objects.all()
    serializer_class = ExportJobSerializer
    resource_name = "reports"

    def create(self, request, *args, **kwargs):
        job = ExportJob.objects.create(
            organization=request.organization,
            name=request.data.get("name", "Export"),
            resource=request.data.get("resource", "customers"),
            filters=request.data.get("filters") or {},
            requested_by=request.user,
        )
        run_export(job)
        return Response(ExportJobSerializer(job).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        job = self.get_object()
        if job.status != "ready" or not job.file_path:
            return Response({"detail": "Export is not ready."}, status=400)
        path = Path(settings.MEDIA_ROOT) / job.file_path
        return FileResponse(open(path, "rb"), as_attachment=True, filename=path.name)


class ReportRunView(APIView):
    resource_name = "reports"

    def post(self, request):
        return Response(
            build_report(request.organization, request.data.get("report_type", "customers"), request.data.get("definition"))
        )
