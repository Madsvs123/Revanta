from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import User
from apps.tenants.models import Organization


@database_sync_to_async
def resolve_user(token, org_id):
    try:
        access = AccessToken(token)
        user = User.objects.filter(id=access["user_id"]).first() or AnonymousUser()
    except Exception:
        user = AnonymousUser()
    organization = Organization.objects.filter(id=org_id).first() if org_id else getattr(user, "last_organization", None)
    return user, organization


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query = parse_qs(scope.get("query_string", b"").decode())
        token = (query.get("token") or [None])[0]
        org_id = (query.get("organization_id") or [None])[0]
        headers = dict(scope.get("headers") or [])
        if not token and headers.get(b"authorization"):
            raw = headers[b"authorization"].decode()
            if raw.startswith("Bearer "):
                token = raw.split(" ", 1)[1]
        user, organization = await resolve_user(token, org_id)
        scope["user"] = user
        scope["organization"] = organization
        return await super().__call__(scope, receive, send)
