from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Invitation, Membership, PasswordResetToken, Role, User
from apps.tenants.models import Organization, OrganizationSetting


def tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


@transaction.atomic
def register_organization(payload):
    if User.objects.filter(email__iexact=payload["email"]).exists():
        raise ValidationError({"email": "An account with this email already exists."})
    user = User.objects.create_user(
        username=payload["email"],
        email=payload["email"].lower(),
        password=payload["password"],
        first_name=payload.get("first_name", ""),
        last_name=payload.get("last_name", ""),
        display_name=payload.get("display_name") or payload.get("first_name") or payload["email"],
    )
    organization = Organization.objects.create(
        name=payload["organization_name"],
        org_type=payload.get("org_type") or Organization.OrgType.RESEARCH,
    )
    Role.ensure_defaults(organization)
    owner = Role.objects.get(organization=organization, slug="owner")
    Membership.objects.create(organization=organization, user=user, role=owner, title="Organization owner")
    OrganizationSetting.objects.get_or_create(organization=organization)
    user.last_organization = organization
    user.save(update_fields=["last_organization"])
    return user, organization


def login_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        user = authenticate(username=email.lower(), password=password)
    if user is None:
        raise AuthenticationFailed("Invalid email or password.")
    return user


@transaction.atomic
def accept_invitation(payload):
    invitation = Invitation.objects.select_related("organization", "role").filter(token=payload["token"]).first()
    if invitation is None or not invitation.is_open:
        raise ValidationError({"token": "Invitation is invalid or expired."})
    user = User.objects.filter(email__iexact=invitation.email).first()
    if user is None:
        user = User.objects.create_user(
            username=invitation.email,
            email=invitation.email,
            password=payload["password"],
            first_name=payload.get("first_name", ""),
            last_name=payload.get("last_name", ""),
            display_name=payload.get("display_name") or invitation.email,
            is_investigator=invitation.is_investigator,
        )
    else:
        user.set_password(payload["password"])
        user.save(update_fields=["password"])
    Membership.objects.update_or_create(
        organization=invitation.organization,
        user=user,
        defaults={"role": invitation.role, "is_active": True, "title": invitation.role.name},
    )
    invitation.accepted_at = invitation.accepted_at or invitation.created_at
    from django.utils import timezone

    invitation.accepted_at = timezone.now()
    invitation.save(update_fields=["accepted_at"])
    user.last_organization = invitation.organization
    user.save(update_fields=["last_organization"])
    return user, invitation.organization


def request_password_reset(email):
    user = User.objects.filter(email__iexact=email).first()
    if user is None:
        return None
    return PasswordResetToken.issue(user)


def reset_password(token, password):
    record = PasswordResetToken.objects.filter(token=token).select_related("user").first()
    if record is None or not record.is_open:
        raise ValidationError({"token": "Reset link is invalid or expired."})
    record.user.set_password(password)
    record.user.save(update_fields=["password"])
    from django.utils import timezone

    record.used_at = timezone.now()
    record.save(update_fields=["used_at"])
    return record.user
