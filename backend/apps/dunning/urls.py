from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.dunning.views import DunningCaseViewSet, DunningPolicyViewSet

router = DefaultRouter()
router.register("dunning/policies", DunningPolicyViewSet, basename="dunning-policies")
router.register("dunning/cases", DunningCaseViewSet, basename="dunning-cases")

urlpatterns = [path("", include(router.urls))))
