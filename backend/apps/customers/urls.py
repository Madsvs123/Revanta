from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.customers.views import (
    BalanceViewSet,
    BillingProfileViewSet,
    CompanyViewSet,
    ContactViewSet,
    CreditViewSet,
    PaymentMethodViewSet,
    TaxInformationViewSet,
)

router = DefaultRouter()
router.register("customers", CompanyViewSet, basename="customers")
router.register("contacts", ContactViewSet, basename="contacts")
router.register("billing-profiles", BillingProfileViewSet, basename="billing-profiles")
router.register("payment-methods", PaymentMethodViewSet, basename="payment-methods")
router.register("tax-information", TaxInformationViewSet, basename="tax-information")
router.register("credits", CreditViewSet, basename="credits")
router.register("balances", BalanceViewSet, basename="balances")

urlpatterns = [path("", include(router.urls))]
