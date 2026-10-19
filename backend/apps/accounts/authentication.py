from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.accounts.models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get("Authorization", "")
        raw = None
        if header.startswith("APIKEY "):
            raw = header.split(" ", 1)[1].strip()
        elif request.headers.get("X-Api-Key"):
            raw = request.headers["X-Api-Key"].strip()
        if not raw:
            return None
        hashed = APIKey.hash_key(raw)
        key = APIKey.objects.select_related("organization", "created_by").filter(hashed_key=hashed).first()
        if not key:
            raise AuthenticationFailed("Invalid or revoked API key.")
        key.last_used_at = timezone.now()
        key.save(update_fields=["last_used_at"])
        request.organization = None
        request.api_key = key
        request.api_key_scopes = key.scopes or []
        return (key.created_by, key)
