from django.http import FileResponse
from pathlib import Path

from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.mixins import TenantQuerysetMixin
from apps.invoicing.models import CreditNote, Invoice, InvoiceAdjustment, RevenueSchedule
from apps.invoicing.serializers import CreditNoteSerializer, InvoiceSerializer, RevenueScheduleSerializer
from apps.invoicing.services import generate_subscription_invoice, issue_credit_note, render_invoice_pdf
from apps.subscriptions.models import Subscription


class InvoiceViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related("company", "subscription").prefetch_related("lines", "taxes", "adjustments")
    serializer_class = InvoiceSerializer
    resource_name = "invoices"
    search_fields = ("number", "company__name")
    filterset_fields = ("status", "company", "currency")
    ordering_fields = ("issue_date", "due_date", "total", "amount_due")

    @action(detail=False, methods=["post"])
    def generate(self, request):
        subscription = Subscription.objects.get(id=request.data["subscription_id"])
        invoice = generate_subscription_invoice(subscription)
        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def adjust(self, request, pk=None):
        invoice = self.get_object()
        adjustment = InvoiceAdjustment.objects.create(
            organization=request.organization,
            invoice=invoice,
            reason=request.data.get("reason", "Manual adjustment"),
            amount=request.data["amount"],
            created_by=request.user,
        )
        invoice.total += adjustment.amount
        invoice.amount_due = max(invoice.total - invoice.amount_paid, 0)
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["post"])
    def void(self, request, pk=None):
        invoice = self.get_object()
        invoice.status = "paid"
        invoice.amount_due = 0
        invoice.save(update_fields=["status", "amount_due", "updated_at"])
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["get"])
    def pdf(self, request, pk=None):
        invoice = self.get_object()
        if not invoice.pdf_path:
            render_invoice_pdf(invoice)
        path = Path(settings.MEDIA_ROOT) / invoice.pdf_path
        return FileResponse(open(path, "rb"), as_attachment=True, filename=f"{invoice.number}.pdf")


class CreditNoteViewSet(TenantQuerysetMixin, viewsets.ModelViewSet):
    queryset = CreditNote.objects.select_related("company", "invoice")
    serializer_class = CreditNoteSerializer
    resource_name = "credit-notes"
    filterset_fields = ("company", "invoice")

    def create(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id=request.data["invoice"])
        note = issue_credit_note(invoice, request.data["amount"], request.data.get("reason", "Credit note"))
        return Response(CreditNoteSerializer(note).data, status=status.HTTP_201_CREATED)


class RevenueScheduleViewSet(TenantQuerysetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = RevenueSchedule.objects.all()
    serializer_class = RevenueScheduleSerializer
    resource_name = "payments"
    filterset_fields = ("company", "invoice", "status")
