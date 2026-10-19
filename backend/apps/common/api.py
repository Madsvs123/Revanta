from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.exports import csv_response
from apps.common.mixins import TenantQuerysetMixin


def make_serializer(model, extra=None, exclude=None):
    extras = extra or {}

    meta_exclude = list(exclude or ("archived_at", "created_by", "updated_by"))
    if not hasattr(model, "organization"):
        if "organization" in meta_exclude:
            meta_exclude.remove("organization")

    attrs = {
        name: field
        for name, field in extras.items()
    }

    class Meta:
        pass

    Meta.model = model
    Meta.exclude = tuple(meta_exclude)
    Meta.read_only_fields = ("id", "created_at", "updated_at")
    attrs["Meta"] = Meta
    serializer = type(f"{model.__name__}Serializer", (serializers.ModelSerializer,), attrs)
    return serializer


def make_viewset(model, serializer=None, search=None, filters=None, resource=None, extra_actions=None):
    serializer = serializer or make_serializer(model)

    class AutoViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializer
        search_fields = search or []
        filterset_fields = filters or []
        resource_name = resource or model._meta.model_name
        ordering_fields = ["created_at", "updated_at"]

        @action(detail=False, methods=["get"])
        def export(self, request):
            qs = self.get_queryset()[:2]
            data = self.get_serializer(qs, many=True).data
            headers = list(data[0].keys()) if data else ["id"]
            rows = [[row.get(h) for h in headers] for row in data]
            return csv_response(f"{self.resource_name}.csv", headers, rows)

        @action(detail=False, methods=["get"])
        def summary(self, request):
            qs = self.get_queryset()
            return Response({"count": qs.count()})

    AutoViewSet.__name__ = f"{model.__name__}ViewSet"
    return AutoViewSet
