from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.commissions.views import AccrualViewSet, CommissionPlanViewSet, CommissionTierViewSet, PayoutViewSet

router = DefaultRouter()
router.register("commission-plans", CommissionPlanViewSet, basename="commission-plans")
router.register("commission-tiers", CommissionTierViewSet, basename="commission-tiers")
router.register("commissions", AccrualViewSet, basename="commissions")
router.register("commission-payouts", PayoutViewSet, basename="commission-payouts")

urlpatterns = [path("", include(router.urls))]
