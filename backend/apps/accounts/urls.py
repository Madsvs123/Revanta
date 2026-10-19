from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import (
    APIKeyViewSet,
    InvitationViewSet,
    LoginView,
    MeView,
    MembershipViewSet,
    RefreshView,
    RegisterView,
    RoleViewSet,
)

router = DefaultRouter()
router.register("roles", RoleViewSet, basename="roles")
router.register("members", MembershipViewSet, basename="members")
router.register("invitations", InvitationViewSet, basename="invitations")
router.register("keys", APIKeyViewSet, basename="api-keys")

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/signin/", LoginView.as_view()),
    path("auth/refresh/", RefreshView.as_view()),
    path("auth/me/", MeView.as_view()),
    path("", include(router.urls)),
]
