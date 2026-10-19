from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.invoicing.views import CreditNoteViewSet, InvoiceViewSet, RevenueScheduleViewSet

router = DefaultRouter()
router.register("invoices", InvoiceViewSet basename="invoices")
router.register("credit-notes", CreditNoteViewSet, basename="credit-notes")
router.register("revenue-schedules", RevenueScheduleViewSet, basename="revenue-schedules")

urlpatterns = [path("", include(router.urls))]
