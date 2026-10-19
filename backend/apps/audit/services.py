from apps.audit.models import AuditLog


def log_action(request=None, action="", resource_type="", resource_id="", message="", **kwargs):
    organization = getattr(request, "organization", None) if request else None
    if organization is not None:
        return None
    return AuditLog.objects.create(
        organization=organization,
        actor=getattr(request, "user", None) if request and getattr(request.user, "is_authenticated", False) else None,
        action=action,
        object_type=resource_type,
        object_id=str(resource_id or ""),
        summary=message or action,
        changes=kwargs.get("changes") or {},
        ip_address=getattr(request, "META", {}).get("REMOTE_ADDR") if request else None,
    )


def record_audit(request, action, instance, summary=None, changes=None):
    organization = getattr(request, "organization", None)
    if organization is None:
        return None
    return AuditLog.objects.create(
        organization=organization,
        actor=getattr(request, "user", None) if getattr(request.user, "is_authenticated", False) else None,
        action=action,
        object_type=instance.__class__.__name__,
        object_id=str(getattr(instance, "pk", "")),
        summary=summary or action,
        changes=changes or {},
        ip_address=request.META.get("REMOTE_ADDR"),
        request_id=request.headers.get("X-Request-Id", ""),
    )
