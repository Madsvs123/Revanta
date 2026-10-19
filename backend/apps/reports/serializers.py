from rest_framework import serializers

from apps.reports.models import ExportJob, SavedReport


class SavedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = ("id", "name", "report_type", "definition", "is_shared", "created_at")


class ExportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportJob
        fields = ("id", "name", "resource", "status", "file_path", "filters", "error", "created_at")
        read_only_fields = ("id", "status", "file_path", "error", "created_at")
