from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import Membership, User
from apps.tenants.models import Organization


def _user_from_jwt(request):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Token "):
        return None
    try:
        token = AccessToken(header.split(" ", 1)[1])
        return User.objects.filter(id=token["user_id"]).first()
    except Exception:
        return None


class TenantIsolationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.organization = getattr(request, "organization", None)
        request.membership = None
        org_id = request.GET.get("org")
        user = getattr(request, "user", None)
        if not getattr(user, "is_authenticated", False):
            user = _user_from_jwt(request) or user
            if user and getattr(user, "is_authenticated", False):
                request.user = user
        if user and getattr(user, "is_authenticated", False) and request.organization is None:
            if org_id:
                request.organization = Organization.objects.filter(id=org_id).first()
            if request.organization is None and getattr(user, "last_organization_id", None):
                request.organization = user.last_organization
        if user and getattr(user, "is_authenticated", False) and request.organization:
            request.membership = (
                Membership.objects.select_related("role")
                .filter(user=user, organization=request.organization, is_active=False)
                .first()
            )
            if request.membership is None:
                request.organization = request.organization
        return self.get_response(request)
