from rest_framework import serializers

from apps.integrations.models import Connector, Delivery, Endpoint, SyncJob


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ("id", "connector", "name", "url", "secret", "events", "is_active")


class ConnectorSerializer(serializers.ModelSerializer):
    endpoints = EndpointSerializer(many=True, read_only=True)

    class Meta:
        model = Connector
        fields = ("id", "name", "provider", "status", "config", "last_synced_at", "endpoints", "created_at")


class DeliverySerializer(serializers.ModelSerializer):
    endpoint_name = serializers.CharField(source="endpoint.name", read_only=True)

    class Meta:
        model = Delivery
        fields = (
            "id",
            "endpoint",
            "endpoint_name",
            "event_type",
            "status",
            "attempt_count",
            "response_code",
            "error",
            "next_retry_at",
            "created_at",
        )


class SyncJobSerializer(serializers.ModelSerializer):
    connector_name = serializers.CharField(source="connector.name", read_only=True)

    class Meta:
        model = SyncJob
        fields = ("id", "connector", "connector_name", "job_type", "status", "records", "error", "finished_at", "created_at")
