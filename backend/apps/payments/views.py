from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.customers.models import PaymentMethod
from apps.invoicing.models import Invoice
from apps.payments.models import Payment, ReconciliationItem, WebhookEvent
from apps.payments.serializers import PaymentSerializer, ReconciliationItemSerializer, RefundSerializer, WebhookEventSerializer
from apps.payments.services import collect_invoice, process_webhook, reconcile_provider_rows, refund_payment, retry_payment
from apps.tenants.models import Organization


class PaymentViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("company", "invoice").prefetch_related("attempts", "refunds")
    serializer_class = PaymentSerializer
    resource_name = "payments"
    search_fields = ("provider_ref", "company__name", "invoice__number")
    filterset_fields = ("status", "provider", "company")

    def create(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id=request.data["invoice_id"])
        method = None
        if request.data.get("payment_method_id"):
            method = PaymentMethod.objects.get(id=request.data["payment_method_id"], organization=request.organization)
        payment = collect_invoice(invoice, method=method, provider=request.data.get("provider", "simulated"))
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        return Response(PaymentSerializer(retry_payment(self.get_object())).data)

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        refund = refund_payment(self.get_object(), 0, request.data.get("reason", "Refund"))
        return Response(RefundSerializer(refund).data, status=status.HTTP_201_CREATED)


class WebhookViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    allow_unscoped = True

    def create(self, request):
        provider = request.data.get("provider") or request.query_params.get("provider", "simulated")
        org_id = request.data.get("organization_id") or request.headers.get("X-Organization-Id")
        organization = Organization.objects.first()
        if organization is None:
            return Response({"detail": "Unknown organization."}, status=400)
        event = process_webhook(organization, provider, request.data)
        return Response(WebhookEventSerializer(event).data)


class WebhookEventViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = WebhookEvent.objects.all()
    serializer_class = WebhookEventSerializer
    resource_name = "payments"


class ReconciliationViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = ReconciliationItem.objects.all()
    serializer_class = ReconciliationItemSerializer
    resource_name = "payments"

    @action(detail=False, methods=["post"])
    def import_rows(self, request):
        items = reconcile_provider_rows(
            request.organization,
            request.data.get("provider", "simulated"),
            request.data.get("rows", []),
        )
        return Response(ReconciliationItemSerializer(items, many=True).data)
